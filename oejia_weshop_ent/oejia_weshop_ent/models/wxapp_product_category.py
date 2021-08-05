# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Category(models.Model):

    _inherit = 'wxapp.product.category'

    tag_id = fields.Many2one('wxapp.product.tag', string='标签')
    is_tag = fields.Boolean(string='关联到标签', default=False)
    alias = fields.Char('别名')

