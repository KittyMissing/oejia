# coding=utf-8
from odoo import models, fields, api, exceptions
from .. import defs

class BlanceLogs(models.Model):

    _name = 'oe.balance.logs'
    _description = u'钱包明细'

    partner_id = fields.Many2one('res.partner', required=True, string='用户')
    log_type = fields.Selection(defs.BalanceLogType.attrs.items(), string='类型', default='default')
    behavior = fields.Selection([('0', '收入'), ('1', '支出')], string='收入/支出', default='0')
    amount = fields.Float('变动金额')
    balance_left = fields.Float('剩余金额')
    remark = fields.Text(string='备注')

    def log_type_show(self):
        return dict(self._fields['log_type'].selection)[self.log_type]
