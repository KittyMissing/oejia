# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Tag(models.Model):

    _name = 'wxapp.product.tag'
    _description = u'商品标签类别'

    name = fields.Char('标签名', required=True, translate=True)
    sequence = fields.Integer(string='排序')
