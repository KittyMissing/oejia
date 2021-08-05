# coding=utf-8
import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):

    _inherit = 'res.partner'

    balance = fields.Float('钱包余额', default=0)
    score = fields.Integer('积分', default=0)

    @api.multi
    def write(self, vals):
        old_score = dict([(obj.id, obj.score) for obj in self])
        old_balance = dict([(obj.id, obj.balance) for obj in self])
        result = super(ResPartner, self).write(vals)
        if '__from_change' in vals:
            vals.pop('__from_change')
        else:
            if 'score' in vals:
                for obj in self:
                    obj.change_score(vals['score']-old_score[obj.id], 'admin', update=False)
            if 'balance' in vals:
                for obj in self:
                    obj.change_balance(vals['balance']-old_balance[obj.id], 'admin', update=False)
        return result

    def change_score(self, score, log_type, update=True):
        if update:
            self.write({'score': self.score + score, '__from_change': True})
        return self.env['oe.score.logs'].sudo().create({
            'partner_id': self.id,
            'log_type':  log_type,
            'behavior': score>0 and '0' or '1',
            'score': abs(score),
            'score_left': self.score,
        })

    def change_balance(self, amount, log_type, update=True):
        if update:
            self.write({'balance': self.balance + amount, '__from_change': True})
        return self.env['oe.balance.logs'].sudo().create({
            'partner_id': self.id,
            'log_type':  log_type,
            'behavior': amount>0 and '0' or '1',
            'amount': abs(amount),
            'balance_left': self.balance,
        })

