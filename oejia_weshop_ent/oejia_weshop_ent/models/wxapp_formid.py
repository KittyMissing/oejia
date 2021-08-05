# coding=utf-8
import json
import logging

from openerp import models, fields, api

from .. import defs

_logger = logging.getLogger(__name__)


class WxappFormid(models.Model):

    _name = 'wxapp.formid'
    _order = "id desc"

    wechat_user_id = fields.Many2one('wxapp.user', string='微信用户')
    formid = fields.Char('表单ID')
    ftype = fields.Selection(defs.FormType.attrs.items(), string='类型', default='form')
    state = fields.Selection([('new', '新建'),('used', '已使用')], string="状态", default='new')
    sent_count = fields.Integer('已发送次数', default=0)

    @api.multi
    def get_available_formid(self):
        for obj in self:
            _logger.info('>>> get_available_formid: %s', obj.id)
            if obj.state=='new':
                obj.write({'state': 'used', 'sent_count': obj.sent_count + 1})
                return obj.formid
