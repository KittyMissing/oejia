# -*- coding: utf-8 -*-

import json

from odoo import http
from odoo.http import request

from .. import defs
from odoo.addons.oejia_weshop.controllers.product import WxappProduct
from odoo.addons.oejia_weshop.controllers.base import dt_convert
from odoo import release

import logging

_logger = logging.getLogger(__name__)

uom_model_name = 'uom.uom'
odoo_ver = release.version_info[0]
if odoo_ver<=10:
    uom_model_name = 'product.uom'

class WxappProductExt(WxappProduct):

    def get_goods_domain(self, category_id, nameLike, **kwargs):
        domain = []
        if kwargs.get('recommendStatus')=='1':
            domain.append(('recommend_status', '=', True))
            kwargs.pop('recommendStatus')
        _category_id = category_id
        if _category_id:
            category_obj = request.env['wxapp.product.category'].sudo().browse(int(_category_id))
            if category_obj.is_tag and category_obj.tag_id:
                domain.append(('tag_ids', 'in', [category_obj.tag_id.id]))
                _category_id = None
        ret = super(WxappProductExt, self).get_goods_domain(_category_id, nameLike, **kwargs)
        ret += domain
        category_ids = []
        if hasattr(request, 'wechat_user') and request.wechat_user:
            category_id = request.wechat_user.category_id
            if category_id:
                category_ids = [e.id for e in category_id]
        if category_ids:
            ret += ['|', ('partner_cate_id', '=', False), ('partner_cate_id', 'in', category_ids)]
        else:
            ret.append(('partner_cate_id', '=', False))
        return ret

    def _product_basic_dict(self, each_goods):
        _logger.info('>>> ent _product_basic_dict')
        ret = super(WxappProductExt, self)._product_basic_dict(each_goods)
        ret['logisticsId'] = each_goods.logistics_id.id or 1
        ret['numberSells'] = each_goods.sold_count
        ret['minScore'] = 0
        if hasattr(each_goods, 'tag_ids'):
            ret['tag_ids'] = [e.id for e in each_goods.tag_ids]
        return ret

    def product_info_ext(self, data, goods, product):
        '''
        goods 产品
        product 产品变体
        '''
        super(WxappProductExt, self).product_info_ext(data, goods, product)
        if goods.enable_uom_select:
            if 'properties' not in data['data']:
                data['data']['properties'] = []
            data['data']['properties'].insert(0, self.get_uom_properties(goods))
        if product:
            data['data']['selectData'] = {
                "price": request.env['product.template'].cli_price(product.get_present_price(1)),
                "score": 0,
                "propertyChildIds": product.attr_val_str,
                "propertyChildNames": product.get_property_str(),
                "stores": product.get_present_qty(),
            }

    def get_uom_properties(self, goods):
        uom_cate = goods.uom_id.category_id
        uoms = request.env[uom_model_name].sudo().search([('category_id', '=', uom_cate.id)])
        ret = {
            "childsCurGoods": [
                {
                    "dateAdd": each_child.create_date,
                    "dateUpdate": each_child.write_date,
                    "id": each_child.id,
                    "name": each_child.name,
                    "paixu": each_child.id,#each_child.sequence,
                    "propertyId": uom_cate.id,
                    "remark": '',#each_child.remark or '',
                    "userId": each_child.create_uid.id
                } for each_child in uoms
            ],
            "dateAdd": uom_cate.create_date,
            "dateUpdate": uom_cate.write_date,
            "id": uom_cate.id,
            "name": u'单位',
            "paixu": uom_cate.id, #each_property.sequence
            "userId": uom_cate.create_uid.id
        }
        return ret

    @http.route('/wxa/<string:sub_domain>/shop/goods/price', auth='public', methods=['GET', 'POST'], csrf=False)
    def price(self, sub_domain, goodsId=False, propertyChildIds=False, **kwargs):
        '''
        选了规格之后请求此接口
        '''
        goods_id = goodsId
        property_child_ids = propertyChildIds
        token = kwargs.get('token', None)
        try:
            ret, entry = self._check_domain(sub_domain)
            if ret:return ret
            self.check_userid(token)

            if not goods_id:
                return self.res_err(300)

            if not property_child_ids:
                return self.res_err(300)

            goods = request.env['product.template'].sudo().browse(int(goods_id))
            rate = 1.0
            if goods.enable_uom_select:
                uom_attr_val_str, property_child_ids = property_child_ids.split(',',1)
                _logger.info('>>> property_child_ids split %s %s', uom_attr_val_str, property_child_ids)
                uom_cate_id, uom_id = uom_attr_val_str.split(':')
                uom = request.env[uom_model_name].sudo().browse(int(uom_id))
                if uom.uom_type!='reference':
                    rate = uom.factor_inv

            if not goods:
                return self.res_err(404)

            price = request.env['product.product'].sudo().search([
                ('product_tmpl_id', '=', goods.id),
                ('attr_val_str', '=', property_child_ids)
            ])

            if not price:
                return self.res_err(404)

            data = {
                "goodsId": goods.id,
                "id": price.id,
                "originalPrice": price.original_price,
                "price": request.env['product.template'].cli_price(price.get_present_price(1)*rate),
                "score": 0,
                "propertyChildIds": price.attr_val_str,
                "stores": price.get_present_qty()
            }
            return self.res_ok(data)

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, str(e))


    @http.route('/wxa/<string:sub_domain>/shop/goods/price/freight', auth='public', methods=['GET'])
    def freight(self, sub_domain, **kwargs):
        try:
            ret, entry = self._check_domain(sub_domain)
            if ret:return ret

            args_key_set = {'logistics_id', 'transport_type', 'province_id', 'city_id', 'district_id'}

            missing_args_key = args_key_set - set(kwargs.keys())
            if missing_args_key:
                return self.res_err(300)

            # 使用order保证运输费是最精确的地址匹配
            transport = request.env(user=1)['oe.district.freight'].search([
                ('default_transportation_id.logistics_id', '=', int(kwargs['logistics_id'])),
                ('default_transportation_id.transport_type', '=',
                 defs.TransportRequestType.attrs[int(kwargs.get('transport_type'))]),
                ('province_id', '=', int(kwargs['province_id'])),
                ('city_id', '=', int(kwargs['city_id'])),
                ('district_id', 'in', [int(kwargs['district_id']) if kwargs['district_id'] else False, False]),
            ], limit=1, order='district_id asc')

            if not transport:
                transport = request.env(user=1)['oe.logistics.freight'].search([
                    ('logistics_id', '=', int(kwargs['logistics_id'])),
                    ('transport_type', '=', defs.TransportRequestType.attrs[int(kwargs.get('transport_type'))]),
                ], limit=1)

            data = {
                "transport_type": int(kwargs.get('transport_type')),
                "firstNumber": transport.less_amount or 0,
                "addAmount": transport.increase_price or 0,
                "firstAmount": transport.less_price or 0,
                "addNumber": transport.increase_amount or 0,
            }
            return self.res_ok(data)

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, str(e))


