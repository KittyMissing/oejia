# coding=utf-8
import json
import logging
import datetime

from openerp import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import release

from .utils import AsyncDB

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):

    _inherit = "sale.order"

    use_score = fields.Integer('使用的积分数量', default=0, copy=False)
    has_refund = fields.Boolean('有售后退换', default=False)
    refund_ids = fields.One2many('wxapp.refund', 'order_id', string='售后记录')
    peisong_type = fields.Selection([('kd', '快递'), ('zq', '到店自取')], string='配送方式', default='kd')

    @api.multi
    def action_confirm(self):
        old_status = self.state
        result = super(SaleOrder, self).action_confirm()

        entry = self.env.ref('oejia_weshop.wxapp_config_data_1')
        for obj in self:
            if not obj.number_goods>0:
                continue
            wechat_users = self.env['wxapp.user'].sudo().search([('partner_id', '=', obj.partner_id.id)])
            if obj.customer_status == 'unpaid':
                for wechat_user in wechat_users:
                    old_vals = {'state': old_status, 'customer_status': obj.customer_status}
                    wechat_user.send_notify(entry, obj, old_vals)
        return result

    @api.multi
    def delivery(self):
        '''
        发货
        '''
        result = super(SaleOrder, self).delivery()

        entry = self.env.ref('oejia_weshop.wxapp_config_data_1')
        for obj in self:
            wechat_users = self.env['wxapp.user'].search([('partner_id', '=', obj.partner_id.id)])
            for wechat_user in wechat_users:
                old_vals = {'state': obj.state, 'customer_status': 'pending'}
                wechat_user.send_notify(entry, obj, old_vals)

        return result

    @api.multi
    def action_paid(self):
        '''
        支付完
        '''
        _logger.info('>>> oejia_weshop_ent action_paid')
        super(SaleOrder, self).action_paid()

        entry = self.env.ref('oejia_weshop.wxapp_config_data_1')
        for obj in self:
            if obj.state!='sale':
                obj.action_confirm()
            wechat_users = self.env['wxapp.user'].search([('partner_id', '=', obj.partner_id.id)])
            for wechat_user in wechat_users:
                old_vals = {'state': obj.state, 'customer_status': 'unpaid'}
                wechat_user.send_notify(entry, obj, old_vals)
        self.paid_event_delay()

    @api.multi
    def action_created(self, data=None):
        '''
        新订单
        '''
        super(SaleOrder, self).action_created(data)
        entry = self.env.ref('oejia_weshop.wxapp_config_data_1')
        for obj in self:
            if not obj.user_id and entry.user_id:
                obj.write({'user_id': entry.user_id.id})
            wechat_users = self.env['wxapp.user'].search([('partner_id', '=', obj.partner_id.id)])
            for wechat_user in wechat_users:
                wechat_user.send_notify(entry, obj, {})
            if entry.auto_cancel_expired_order:
                self.check_expired_order_delay(obj.partner_id.id)
            if release.version_info[0]<=0:
                self.env['ir.cron'].sudo().create({
                    'name': u'订单超时检查 %s'%obj.name,
                    'user_id': self.env.uid,
                    'model': self._name,
                    'active': True,
                    'priority': 2,
                    'doall': True,
                    'numbercall': 1,
                    'nextcall': (datetime.datetime.utcnow() + datetime.timedelta(minutes=31)).strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'interval_type': 'minutes',
                    'function': 'check_expired_order',
                    'args': repr([obj.partner_id.id])
                })
        self.create_event_delay()

    @api.multi
    def action_cancel(self):
        '''
        关闭订单
        '''
        result = super(SaleOrder, self).action_cancel()
        entry = self.env.ref('oejia_weshop.wxapp_config_data_1')
        for obj in self:
            wechat_users = self.env['wxapp.user'].search([('partner_id', '=', obj.partner_id.id)])
            for wechat_user in wechat_users:
                wechat_user.send_notify_close(entry, obj)
        self.cancel_event_delay()
        return result

    @api.multi
    def refund_window_action(self):
        refunds = self.mapped('refund_ids')
        action = self.env.ref('oejia_weshop_ent.wxapp_refund_action_623').read()[0]
        action['views'] = [(self.env.ref('oejia_weshop_ent.wxapp_refund_view_form_1804').id, 'form')]
        action['res_id'] = refunds[0].id
        return action

    @api.model
    def check_expired_order(self, partner_id=None):
        '''
        超过30分钟订单自动取消
        '''
        _logger.info('>>> check_expired_order')
        domain = [
            ('customer_status', '=', 'unpaid'),
            ('create_date', '<', fields.Datetime.to_string(fields.datetime.now() - datetime.timedelta(minutes=30))),
            ('state', 'in', ['draft', 'sent']),
            ('number_goods', '>', 0),
        ]
        if partner_id:
            domain.append(('partner_id', '=', partner_id))
        expired_orders = self.search(domain)
        _logger.info('>>> expired_orders %s domain %s', expired_orders, domain)
        expired_orders.action_cancel()
        return [e.id for e in expired_orders]

    @AsyncDB(countdown=31*60)
    @api.model
    def check_expired_order_delay(self, partner_id=None):
        return self.check_expired_order(partner_id)

    @AsyncDB(countdown=10)
    @api.multi
    def create_event_delay(self):
        return self.create_event()

    @api.multi
    def create_event(self):
        for obj in self:
            for line in obj.order_line:
                product_tmpl = line.product_id.product_tmpl_id
                product_tmpl.write({'sold_count': product_tmpl.sold_count + line.product_uom_qty})

    @AsyncDB(countdown=10)
    @api.multi
    def paid_event_delay(self):
        return self.paid_event()

    @api.multi
    def paid_event(self):
        pass

    @AsyncDB(countdown=10)
    @api.multi
    def cancel_event_delay(self):
        return self.cancel_event()

    @api.multi
    def cancel_event(self):
        pass
