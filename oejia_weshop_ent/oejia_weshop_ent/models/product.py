# coding=utf-8
import json
import logging

from odoo.http import request
from openerp import models, fields, api

_logger = logging.getLogger(__name__)

USE_ALONE_QTY = None


class ProductTemplate(models.Model):

    _inherit = "product.template"

    wxpp_category_id = fields.Many2one('wxapp.product.category', string='电商分类', ondelete='set null', domain=[('is_tag', '=', False)])
    logistics_id = fields.Many2one('oe.logistics', string='运费模板')
    partner_cate_id = fields.Many2one('res.partner.category', string='可见客户类别')
    no_qty_check = fields.Boolean('无库存时允许下单', default=True)
    enable_uom_select = fields.Boolean('允许多计量单位选择', default=False)
    sold_count = fields.Integer('已售出数量', default=0)
    main_img = fields.Char('主图', compute='_get_main_image', store=True)
    images_data = fields.Char('图片', compute='_get_multi_images', store=True)
    tag_ids = fields.Many2many('wxapp.product.tag', string='标签')

    def get_present_qty(self):
        if self.no_qty_check:
            return 999
        else:
            return self.get_qty()

    def get_qty(self):
        if hasattr(request, 'wechat_user') and request.wechat_user:
            user = request.wechat_user.user_id
            if user:
                self = self.with_context(force_company=user.company_id.id)
        return self.virtual_available

    def _compute_qty_show(self):
        for obj in self:
            obj.qty_show = obj.get_qty()

    def change_qty(self, val):
        #self.write({'qty_public_tpl': self.qty_public_tpl + val})
        pass

    def get_present_price(self, quantity):
        if hasattr(request, 'wechat_user') and request.wechat_user:
            partner_id = request.wechat_user.partner_id
            user = request.wechat_user.user_id
            if user:
                partner_id = partner_id.with_context(force_company=user.company_id.id)
            return partner_id.property_product_pricelist.get_product_price(self, quantity, partner_id)
        else:
            return super(ProductTemplate, self).get_present_price(quantity)

    @api.depends('image_256')
    def _get_main_image(self):
        _logger.info('>>> _get_main_image')
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for obj in self:
            obj.main_img = '%s/web/attach/image?model=product.template&id=%s&field=image_256#'%(base_url, obj.id)

    @api.depends('image_256')
    def _get_multi_images(self):
        _logger.info('>>> _get_multi_images')
        base_url=self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for product in self:
            _list = []
            if hasattr(product, 'product_image_ids'):
                for obj in product.product_image_ids:
                    _dict = {
                        "id": obj.id,
                        "goodsId": product.id,
                        "pic": '%s/web/attach/image?model=product.image&id=%s&field=image_1024#'%(base_url, obj.id)
                    }
                    _list.append(_dict)
            _list.append({
                'id': product.id,
                'goodsId': product.id,
                'pic': '%s/web/attach/image?model=product.template&id=%s&field=image_1024#'%(base_url, product.id)
            })
            product.images_data =  json.dumps(_list)

    @api.model
    def cli_price(self, price):
        price_need_login = False
        if price_need_login:
            if not (hasattr(request, 'wechat_user') and request.wechat_user):
                return '询价'
        return super(ProductTemplate, self).cli_price(price)

class ProductProduct(models.Model):

    _inherit = "product.product"

    # attr_val_str 字符'property_id1:value_id1,property_id2:value_id2,'

    @api.multi
    @api.depends('product_template_attribute_value_ids')
    def _compute_attr_val_str(self):
        for obj in self:
            _str = ''
            attr_val_list = obj.product_template_attribute_value_ids.sorted(key=lambda o: o.attribute_id.id)
            for o in attr_val_list:
                _str += '%s:%s,'%(o.attribute_id.id, o.product_attribute_value_id.id)
            obj.attr_val_str = _str

    def get_property_str(self):
        return ', '.join(['%s: %s'%(e.attribute_id.name, e.name) for e in self.product_template_attribute_value_ids])



    def get_present_qty(self):
        if self.no_qty_check:
            return 999
        else:
            return self.get_qty()

    def get_qty(self):
        if hasattr(request, 'wechat_user') and request.wechat_user:
            user = request.wechat_user.user_id
            if user:
                self = self.with_context(force_company=user.company_id.id)
        return self.virtual_available

    def change_qty(self, val):
        # self.write({'qty_public': self.qty_public + val})
        pass

    def get_present_price(self, quantity):
        if hasattr(request, 'wechat_user') and request.wechat_user:
            partner_id = request.wechat_user.partner_id
            user = request.wechat_user.user_id
            if user:
                partner_id = partner_id.with_context(force_company=user.company_id.id)
            return partner_id.property_product_pricelist.get_product_price(self, quantity, partner_id)
        else:
            return super(ProductProduct, self).get_present_price(quantity)
