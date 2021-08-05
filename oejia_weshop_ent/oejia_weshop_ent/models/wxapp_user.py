# coding=utf-8
import json
import logging
import datetime

from openerp import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import release

from .utils import AsyncDB

_logger = logging.getLogger(__name__)


class WxappUser(models.Model):

    _inherit = 'wxapp.user'

    user_id = fields.Many2one('res.users', string='关联的用户')
    #balance = fields.Float('钱包余额', default=0)
    formid_ids = fields.One2many('wxapp.formid', 'wechat_user_id', string='表单ID记录')

    def bind_mobile(self, mobile):
        partner = self.env['res.partner'].sudo().search([('mobile', '=', mobile), ('type', '!=', 'delivery')], limit=1)
        if partner:
            self.write({
                'partner_id': partner.id,
                'category_id': [(4, self.env.ref('oejia_weshop.res_partner_category_data_1').sudo().id)],
            })
        else:
            self.partner_id.write({'mobile': mobile})

    @AsyncDB()
    @api.model
    def send_template_msg(self, wechat_user_id, entry_id, template_id, postJson, url):
        _logger.info('>>> send_template_msg %s %s %s %s %s', wechat_user_id, entry_id, template_id, postJson, url)
        self = self.sudo()
        wechat_user = self.browse(wechat_user_id)
        open_id = wechat_user.open_id
        from wechatpy.client import WeChatClient
        entry = self.env['wxapp.config'].browse(entry_id)
        client = WeChatClient(entry.app_id, entry.secret)
        try:
            res =client.wxa.send_subscribe_message(open_id, template_id, postJson, url)
            _logger.info('>>> send_template_msg %s %s return %s', open_id, template_id, res)
        except:
            import traceback;traceback.print_exc()

    def send_notify_close(self, entry, order, old_vals=None):
        '''
        订单关闭时的通知
        '''
        from odoo.addons.oejia_weshop.controllers.base import dt_convert
        template_id = entry.msgtpl_order_closed
        if not template_id:
            return
        keys = self.env['wxapp.msg.tpl'].sudo().get_keys(template_id, 3)
        postJson = {
            keys[0] or 'character_string1': {'value': order.name},
            #'keyword2': {'value': round(order.amount_total, 2)},
            keys[1] or 'time3': {'value': dt_convert(order.create_date)},
            keys[2] or 'thing5': {'value': u'超时关闭'},
        }
        url = '/pages/order-list/index'
        self.send_template_msg(self.id, entry.id, template_id, postJson, url)

    @api.multi
    def send_notify(self, entry, order, old_vals):
        from odoo.addons.oejia_weshop.controllers.base import dt_convert
        if not old_vals:
            # 新订单通知
            template_id = entry.msgtpl_order_created
            if not template_id:
                return
            keys = self.env['wxapp.msg.tpl'].sudo().get_keys(template_id, 4)
            postJson = {
                keys[0] or 'character_string1': {'value': order.name},
                keys[1] or 'amount3': {'value': round(order.amount_total, 2)},
                keys[2] or 'date2': {'value': dt_convert(order.create_date)},
                keys[3] or 'phrase4': {'value': u'待支付'},
            }
            url = '/pages/order-list/index'
            self.send_template_msg(self.id, entry.id, template_id, postJson, url)

        if old_vals.get('customer_status')=='pending' and order.customer_status=='unconfirmed':
            # 已发货通知
            template_id = entry.msgtpl_order_delivery
            if not template_id:
                return
            keys = self.env['wxapp.msg.tpl'].sudo().get_keys(template_id, 5)
            postJson = {
                keys[0] or 'character_string2': {'value': order.name},
                #'keyword2': {'value': round(order.amount_total, 2)},
                keys[1] or 'phrase4': {'value': order.shipper_id.name},
                keys[2] or 'character_string3': {'value': order.shipper_no},
                keys[3] or 'date1': {'value': dt_convert(datetime.datetime.utcnow())},
                keys[4] or 'thing8': {'value': order.partner_shipping_id.street},
            }
            url = '/pages/order-list/index'
            self.send_template_msg(self.id, entry.id, template_id, postJson, url)

        if old_vals.get('customer_status')=='unpaid' and order.customer_status=='pending':
            # 已支付成功通知
            template_id = entry.msgtpl_order_paid
            if not template_id:
                return
            keys = self.env['wxapp.msg.tpl'].sudo().get_keys(template_id, 4)
            postJson = {
                keys[0] or 'character_string1': {'value': order.name},
                keys[1] or 'amount3': {'value': round(order.amount_total, 2)},
                keys[2] or 'date2': {'value': dt_convert(order.create_date)},
                keys[3] or 'thing6': {'value': u'已支付'},
            }
            url = '/pages/order-list/index'
            self.send_template_msg(self.id, entry.id, template_id, postJson, url)

        if old_vals.get('state')!='sale' and order.state=='sale' and order.customer_status == 'unpaid':
            # (待付款提醒)确定为销售订单且未支付时的通知
            template_id = entry.msgtpl_order_confirmed
            if not template_id:
                return
            keys = self.env['wxapp.msg.tpl'].sudo().get_keys(template_id, 4)
            postJson = {
                keys[0] or 'character_string1': {'value': order.name},
                keys[1] or 'amount4': {'value': round(order.amount_total, 2)},
                keys[2] or 'date3': {'value': dt_convert(order.create_date)},
                keys[3] or 'thing5': {'value': u'订单已确认，请尽快支付'},
            }
            url = '/pages/order-list/index'
            self.send_template_msg(self.id, entry.id, template_id, postJson, url)
