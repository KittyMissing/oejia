# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

from .. import defs


class Logistics(models.Model):

    _name = 'oe.logistics'
    _description = u'运费模板'

    name = fields.Char('名称', required=True)
    by_self = fields.Boolean('商家自送')
    free = fields.Boolean('是否包邮')
    valuation_type = fields.Selection(defs.LogisticsValuationType.attrs.items(), string='计价类型', default=defs.LogisticsValuationType.by_amount)
    free_limitation_amount = fields.Float('金额')
    fare = fields.Float('运费')

    transportation_ids = fields.One2many('oe.logistics.freight', 'logistics_id', string='运送费用')
    district_transportation_ids = fields.One2many('oe.district.freight', 'logistics_id', string='区域运送费用')
