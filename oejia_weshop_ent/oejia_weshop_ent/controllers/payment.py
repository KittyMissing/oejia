# -*- coding: utf-8 -*-

import time
import json
import xmltodict

from odoo import http, exceptions
from odoo.http import request

from .. import defs
from odoo.addons.oejia_weshop.controllers.base import BaseController

from ..rpc.pay import WeixinPay, build_pay_sign

import logging

_logger = logging.getLogger(__name__)




class WxappPayment(http.Controller, BaseController):

    @http.route('/wxa/<string:sub_domain>/pay/wx/wxapp', auth='public', methods=['GET','POST'], csrf=False, type='http')
    def get_pay_data(self, sub_domain, **kwargs):
        '''
        发起支付
        '''
        token = kwargs.pop('token', None)
        try:
            res, wechat_user, entry = self._check_user(sub_domain, token)
            if res:return res

            config = request.env(user=1)['wxapp.config']
            app_id = entry.get_config('app_id')
            wechat_pay_id = entry.get_config('wechat_pay_id')
            wechat_pay_secret = entry.get_config('wechat_pay_secret')

            if not app_id:
                return self.res_err(404)

            if not wechat_pay_id or not wechat_pay_secret:
                return request.make_response(json.dumps({'code': 404, 'msg': '未设置wechat_pay_id和wechat_pay_secret'}))

            args_key_set = {'nextAction', 'money'}

            missing_args_key = args_key_set - set(kwargs.keys())
            if missing_args_key:
                return self.res_err(600)

            order_id = json.loads(kwargs['nextAction'])['id']
            order_id = int(order_id)
            order = request.env(user=1)['sale.order'].search([
                ('id', '=', order_id)
            ])
            pay_money = kwargs['money'] #order.total
            # check pay_money>=order.total

            old_payment_count = request.env(user=1)['wxapp.payment'].search_count([
                ('order_id','=', order_id)
            ])
            out_trade_no = u'{}'.format(order.name)
            if old_payment_count>0:
                out_trade_no = '%s-%s'%(out_trade_no, old_payment_count)

            payment = request.env(user=1)['wxapp.payment'].create({
                'payment_number': out_trade_no,
                'order_id': order_id,
                'wechat_user_id': wechat_user.id,
                'price': float(pay_money)
            })

            mall_name = u'%s %s'%(entry.get_config('mall_name') or u'OE商城', order.name)
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            wxpay = WeixinPay(appid=app_id, mch_id=wechat_pay_id, partner_key=wechat_pay_secret)
            unified_order = wxpay.unifiedorder(
                body=mall_name,
                total_fee=int(round(float(pay_money) * 100)),
                notify_url=u'{base_url}/wxa/{sub_domain}/pay/notify'.format(base_url=base_url, sub_domain=sub_domain),
                openid=u'{}'.format(wechat_user.open_id),
                out_trade_no=out_trade_no

            )
            _logger.info('WeixinPay return %s'%unified_order)
            if unified_order['return_code'] == 'SUCCESS' and not unified_order['result_code'] == 'FAIL':
                time_stamp = str(int(time.time()))
                response = request.make_response(
                    headers={
                        "Content-Type": "json"
                    },
                    data=json.dumps({
                        "code": 0,
                        "data": {
                            'timeStamp': str(int(time.time())),
                            'nonceStr': unified_order['nonce_str'],
                            'prepayId': unified_order['prepay_id'],
                            'sign': build_pay_sign(app_id, unified_order['nonce_str'], unified_order['prepay_id'],
                                                   time_stamp, wechat_pay_secret)
                        },
                        "msg": "success"
                    })
                )
            else:
                if unified_order.get('err_code') == 'ORDERPAID':
                    order = payment.order_id
                    order.write({'status': 'pending'})
                    #mail_template = request.env.ref('oejia_weshop.wechat_mall_order_paid')
                    #mail_template.sudo().send_mail(order.id, force_send=True, raise_exception=False)
                    payment.unlink()
                return request.make_response(
                    json.dumps({'code': -1, 'msg': unified_order.get('err_code_des', unified_order['return_msg'])})
                )

            return response
        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, str(e))


    def _res_xml(self, code, msg):
        response = request.make_response(
            headers={
                "Content-Type": "application/xml"
            },
            data=xmltodict.unparse({
                'xml': {
                    u'return_code': code,
                    u'return_msg': msg
                }
            })
        )
        return response

    @http.route('/wxa/<string:sub_domain>/pay/notify', auth='public', methods=['POST', 'GET'], csrf=False, type='http')
    def notify(self, sub_domain, **kwargs):
        try:
            ret, entry = self._check_domain(sub_domain)
            if ret:
                return self._res_xml('FAIL', '参数格式校验错误')

            xml_data = request.httprequest.stream.read()
            data = xmltodict.parse(xml_data)['xml']
            if data['return_code'] == 'SUCCESS':
                data.update({'status': defs.PaymentStatus.success})

                payment = request.env['wxapp.payment'].sudo().search([('payment_number', '=', data['out_trade_no'])])
                order = payment.order_id
                payment.write(data)
                if payment.price > order.total:
                    request.env['sale.order.line'].sudo().create({
                        'order_id': order.id,
                        'product_id': request.env.ref('oejia_weshop_ent.product_product_wechat_pay_fee').id,
                        'price_unit': payment.price - order.total,
                        'product_uom_qty': 1,
                    })
                order.action_paid()

                #mail_template = request.env.ref('oejia_weshop.wechat_mall_order_paid')
                #mail_template.sudo().send_mail(order.id, force_send=True, raise_exception=False)
            else:
                data.update({'status': defs.PaymentStatus.fail})

                payment = request.env['wxapp.payment'].sudo().search([('payment_number', '=', data['out_trade_no'])])
                order = payment.order_id
                payment.write(data)
                order.write({'customer_status': 'unpaid'})

            return self._res_xml(u'SUCCESS', u'SUCCESS')

        except Exception as e:
            _logger.exception(e)
            return self._res_xml(u'FAIL', u'服务器内部错误')


    @http.route('/wxa/<string:sub_domain>/order/pay', auth='public', method=['POST'], csrf=False)
    def pay(self, sub_domain, token=None, orderId=None, **kwargs):
        order_id = orderId
        try:
            res, wechat_user, entry = self._check_user(sub_domain, token)
            if res:return res

            if not order_id:
                return self.res_err(300)

            order = request.env['sale.order'].sudo().search([
                ('partner_id', '=', wechat_user.partner_id.id),
                ('id', '=', int(order_id))
            ])

            if not order:
                return self.res_err(404)

            wechat_user.write({'balance': wechat_user.balance - order.amount_total})
            order.action_paid()
            return request.make_response(json.dumps({'code': 0, 'msg': 'success'}))

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, e.name)
