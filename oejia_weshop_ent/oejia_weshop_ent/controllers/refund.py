# -*- coding: utf-8 -*-

import json
import base64

from odoo import http
from odoo.http import request

from .. import defs
from odoo.addons.oejia_weshop.controllers.base import BaseController

import logging

_logger = logging.getLogger(__name__)


class Refund(http.Controller, BaseController):

    @http.route('/wxa/<string:sub_domain>/order/refundApply/info', auth='public', method=['GET', 'POST'], csrf=False)
    def info(self, sub_domain, token, orderId, **kwargs):
        order_id = orderId
        try:
            res, wechat_user, entry = self._check_user(sub_domain, token)
            if res:return res

            obj = request.env['wxapp.refund'].sudo().search([('order_id', '=', int(order_id))], order='id desc', limit=1)
            if not obj:
                return self.res_ok([])
            info = {
                "baseInfo": {
                    "amount": obj.amount,
                    "dateAdd": obj.create_date,
                    "id": obj.id,
                    "logisticsStatus": obj.logistics_status,
                    "logisticsStatusStr": dict(obj._fields['logistics_status'].selection)[obj.logistics_status],
                    "orderId": obj.order_id.id,
                    "reason": obj.reason,
                    "remark": obj.remark,
                    "status": obj.status,
                    "statusStr": defs.RefundStatus.attrs[obj.status],
                    "type": obj.rtype,
                    "typeStr": dict(obj._fields['rtype'].selection)[obj.rtype],
                    "uid": obj.wechat_user_id.id,
                    "userId": 0,
                },
                "pics": [{
                    "applyId": obj.id,
                    "id": img.id,
                    "orderId": obj.order_id.id,
                    "pic": img.get_image_url(),
                    "uid": obj.wechat_user_id.id,
                    "userId":0,
                } for img in obj.image_ids]
            }
            return self.res_ok([info])

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, str(e))

    @http.route('/wxa/<string:sub_domain>/order/refundApply/apply', auth='public', method=['POST'], csrf=False)
    def apply(self, sub_domain, token, orderId, **kwargs):
        order_id = orderId
        try:
            res, wechat_user, entry = self._check_user(sub_domain, token)
            if res:return res

            order = request.env['sale.order'].sudo().search([('id', '=', int(order_id))], limit=1)
            refund = request.env['wxapp.refund'].sudo().search([('order_id', '=', int(order_id)), ('status', '=', '0')], order='id desc', limit=1)
            if refund:
                return self.res_err(20000, '请勿重复申请')
            obj = request.env['wxapp.refund'].sudo().create({
                'order_id': order.id,
                'rtype': str(kwargs.get('type')),
                'logistics_status': str(kwargs.get('logisticsStatus')),
                'reason': kwargs.get('reason'),
                'remark': kwargs.get('remark'),
                'amount': kwargs.get('amount'),
                'wechat_user_id': wechat_user.id,
            })
            order.write({'has_refund': True})
            pic = kwargs.get('pic')
            if pic:
                ids = pic.split(',')
                ids = [int(e) for e in ids]
                request.env['wxapp.refund.image'].sudo().search([('id', 'in', ids)]).write({'refund_id': obj.id})

            return self.res_ok()

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, str(e))

    @http.route('/wxa/<string:sub_domain>/order/refundApply/cancel', auth='public', method=['POST'], csrf=False)
    def cancel(self, sub_domain, token, orderId, **kwargs):
        order_id = orderId
        try:
            res, wechat_user, entry = self._check_user(sub_domain, token)
            if res:return res

            order = request.env['sale.order'].sudo().search([('id', '=', int(order_id))], limit=1)
            refund = request.env['wxapp.refund'].sudo().search([('order_id', '=', int(order_id)), ('status', '=', '0')], order='id desc', limit=1)
            refund.write({'status': '1'})

            return self.res_ok()

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, str(e))


    @http.route('/wxa/<string:sub_domain>/dfs/upload/file', auth='public', methods=['POST'], csrf=False, type='http')
    def upload_file(self, sub_domain, **kwargs):
        _logger.info('>>> supplier upload %s', kwargs)

        token = kwargs.pop('token', None)
        res, wechat_user, entry = self._check_user(sub_domain, token)
        if res:return res

        _file = kwargs.get('upfile',None)
        if _file:
            obj = request.env['wxapp.refund.image'].sudo().create({
                'name': _file.filename,
                'image': base64.encodestring(_file.read()),
            })
            data = {
                "msg": "SUCCESS",
                "originalName": _file.filename,
                "size": "14071",
                "name": _file.filename,
                "type": ".jpg",
                "url": str(obj.id),
            }

        return self.res_ok(data)
