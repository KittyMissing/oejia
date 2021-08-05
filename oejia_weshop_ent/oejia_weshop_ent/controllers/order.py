# -*- coding: utf-8 -*-

import json
import datetime
import pytz

from odoo import http, exceptions
from odoo.http import request

from .. import defs
from odoo.addons.oejia_weshop.controllers.order import WxappOrder
from odoo.addons.oejia_weshop.controllers.base import BaseController, UserException
from odoo import release

import logging

_logger = logging.getLogger(__name__)


class WxappOrderExt(WxappOrder):

    def calculate_goods_fee(self, goods, amount, property_child_ids, calculate):
        rate = 1.0
        uom = None
        if goods.enable_uom_select:
            uom_attr_val_str = ''
            if property_child_ids:
                _ls = property_child_ids.split(',', 1)
                if len(_ls)>1:
                    uom_attr_val_str, property_child_ids = _ls
                    _logger.info('>>> property_child_ids split %s %s', uom_attr_val_str, property_child_ids)
            if uom_attr_val_str:
                uom_cate_id, uom_id = uom_attr_val_str.split(':')
                uom_model_name = 'uom.uom'
                _ver = release.version_info[0]
                if _ver<=10:
                    uom_model_name = 'product.uom'
                uom = request.env[uom_model_name].sudo().browse(int(uom_id))
                if uom.uom_type!='reference':
                    rate = uom.factor_inv
        each_goods_total, line_dict = super(WxappOrderExt, self).calculate_goods_fee(goods, amount, property_child_ids, calculate)
        line_dict['price_unit'] = line_dict['price_unit'] * rate
        if uom:
            line_dict['product_uom'] = uom.id
        _logger.info('>>> ent calculate_goods_fee %s %s', each_goods_total, line_dict)
        return each_goods_total*rate, line_dict

    def _transportation_algorithm(self, logistics_id, amount, transport_type, province_id, city_id, district_id):
        _logger.info('>>> _transportation_algorithm %s %s %s', logistics_id.transportation_ids, transport_type, [e.transport_type for e in logistics_id.transportation_ids])
        # 保证运输费是最精确的地址匹配
        transport = logistics_id.district_transportation_ids.filtered(
            lambda r: r.default_transportation_id.transport_type == defs.TransportRequestType.attrs[transport_type]
                      and r.province_id.id == province_id
                      and r.city_id.id == city_id
                      and r.district_id.id in [district_id, False]
        ).sorted(lambda r: not r.district_id)

        if not transport:
            transport = logistics_id.transportation_ids.filtered(
                lambda r: r.transport_type == defs.TransportRequestType.attrs[transport_type]
            )

        if not transport:
            return 0

        transport = transport[0]

        if amount <= transport.less_amount:
            return transport.less_price
        else:
            if transport.increase_amount:
                increase_price = \
                    int(((amount - transport.less_amount) / transport.increase_amount)) * transport.increase_price
            else:
                increase_price = transport.increase_price
            return transport.less_price + increase_price

    def _order_basic_dict(self, each_order):
        ret = super(WxappOrderExt, self)._order_basic_dict(each_order)
        ret['state'] = defs.OrderResponseState.attrs.get(each_order.state, '')
        ret['has_refund'] = each_order.has_refund
        return ret

    def get_orders_domain(self, status, **kwargs):
        if str(status)=='0':
            if kwargs['entry'].auto_cancel_expired_order:
                request.env['sale.order'].sudo().check_expired_order(request.wechat_user.partner_id.id)
        ret = super(WxappOrderExt, self).get_orders_domain(status, **kwargs)
        has_refund = kwargs.get('hasRefund')
        if has_refund=='true':
            ret.append(('has_refund', '=', True))
        if has_refund=='false':
            ret.append(('has_refund', '=', False))
        return ret

    def pre_check(self, entry, wechat_user, post_data):
        if entry.enable_no_service_period:
            now_utc = datetime.datetime.now()
            now_utc = now_utc.replace(tzinfo=pytz.timezone('UTC'))
            now = now_utc.astimezone(pytz.timezone('Etc/GMT-8'))
            now = now.replace(tzinfo=None)

            start = datetime.datetime(now.year, now.month, now.day, entry.no_service_start_hour, entry.no_service_start_minute, 0)
            end = start + datetime.timedelta(minutes=entry.no_service_long)

            _logger.info('>>> enable_no_service_period start %s end %s now %s', start, end, now)
            if now>=start and now<=end:
                return self.res_err(-3, u'当前时间暂不能提交订单')
        _logger.info('>>> oejia_weshop_ent pre_check')
        if post_data.get('peisongType')!='zq':
            if 'provinceId' not in post_data:
                return self.res_err(-3, u'请指定收货地址')
        ret = super(WxappOrderExt, self).pre_check(entry, wechat_user, post_data)
        return ret

    def calculate_order_logistics(self, wechat_user, order_dict, order_lines):
        """
        计算物流费用
        """
        ret = super(WxappOrderExt, self).calculate_order_logistics(wechat_user, order_dict, order_lines)
        objs = request.env['oe.logistics'].sudo().search([('valuation_type', '=', 'by_amount')], order="id desc")
        if not objs:
            return
        obj = objs[0]
        if obj.free:
            return

        logistics_id = obj

        # 按订单额计数
        amount = order_dict['goods_price']
        transport_type = 0 #express

        return self._transportation_algorithm(logistics_id, amount, transport_type, order_dict['province_id'], order_dict['city_id'], order_dict['district_id'])

    def after_calculate(self, wechat_user, order_dict, order_lines):
        _logger.info('>>> oejia_weshop_ent after_calculate')
        super(WxappOrderExt, self).after_calculate(wechat_user, order_dict, order_lines)
        order_dict['peisong_type'] = order_dict.pop('peisongType') if 'peisongType' in order_dict else 'kd'

        if wechat_user.user_id:
            order_dict['company_id'] = wechat_user.user_id.company_id.id
            if 'stock.warehouse' in request.env:
                order_dict['warehouse_id'] = request.env['stock.warehouse'].sudo().search([('company_id', '=', order_dict['company_id'])], limit=1).id

