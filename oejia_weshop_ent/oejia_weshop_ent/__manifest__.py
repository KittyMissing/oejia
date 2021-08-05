# -*- coding: utf-8 -*-
{
    'name': "OE商城企业版",
    'version': '1.0.0',
    'category': '',
    'summary': 'Odoo OE商城企业版扩展',
    'author': 'Oejia',
    'website': 'http://www.oejia.net/',
    'application': True,
    'depends': ['oejia_weshop', 'sale_stock'],
    'external_dependencies': {
        'python': ['wechatpy'],
    },
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
        'views/oe_logistics_views.xml',
        'views/wxapp_config_views.xml',
        'views/res_partner_views.xml',
        'views/oe_balance_logs_views.xml',
        'views/oe_score_logs_views.xml',
        'views/wxapp_user_views.xml',
        'views/wxapp_refund_views.xml',
        'views/wxapp_refund_image_views.xml',
        'views/sale_order_views.xml',
        'views/wxapp_msg_tpl_views.xml',
        'views/wxapp_product_category_views.xml',
        'views/wxapp_product_tag_views.xml',

        'data/product_product_datas.xml',
    ],
    'demo': [
    ],
    'images': [],
    'description': """
    """,
}
