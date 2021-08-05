# coding=utf-8
import json
import logging

from openerp import models, fields, api

from .. import defs

_logger = logging.getLogger(__name__)


class WxappRefund(models.Model):

    _name = 'wxapp.refund'
    _description = u'售后记录'
    _order = 'id desc'

    order_id = fields.Many2one('sale.order', string='订单', required=True)
    amount = fields.Float('退款金额', requried=True)
    logistics_status = fields.Selection([('0', '未收到货'),('1', '已收到货')], string="货物状态", default='0')
    reason = fields.Char('售后原因')
    remark = fields.Text('售后说明')
    status = fields.Selection(defs.RefundStatus.attrs.items(), string='状态', default=defs.RefundStatus.pending)
    rtype = fields.Selection([('0', '仅退款'),('1', '退货退款'),('2', '换货')], string="售后类型", default='0')
    wechat_user_id = fields.Many2one('wxapp.user', string='客户', required=True)
    image_ids = fields.One2many('wxapp.refund.image', 'refund_id', string='图片')

    @api.multi
    def to_refused(self):
        self.write({'status': '2'})

    @api.multi
    def to_doing(self):
        self.write({'status': '3'})

    @api.multi
    def to_completed(self):
        self.write({'status': '4'})


class RefundImage(models.Model):

    _name = 'wxapp.refund.image'
    _description = u'售后图片'

    name = fields.Char('名称')
    image = fields.Binary('图片', attachment=True)
    refund_id = fields.Many2one('wxapp.refund', '售后记录')

    def get_image_url(self):
        base_url=self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return '%s/web/image/wxapp.refund.image/%s/image/'%(base_url, self.id)
