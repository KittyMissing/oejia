# -*- coding: utf-8 -*-

from odoo import models, fields, api

from .. import defs


class Payment(models.Model):

    _inherit = 'wxapp.payment'

    user_id = fields.Many2one(related='wechat_user_id.user_id', string='用户', readonly=True)
