# coding=utf-8

import logging
import base64
import werkzeug

import odoo
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


DEFAULT_IMG_URL = '/web/static/src/img/placeholder.png'


class Image(http.Controller):

    @http.route(['/web/attach/image'], type='http', auth="public")
    def attachment_image(self, model=None, field=None, id=None, unique=None):
        if not(model and field and id) or model not in ['product.template', 'product.image']:
            return werkzeug.utils.redirect(DEFAULT_IMG_URL, code=302)
        obj = request.env['ir.attachment'].sudo().search([('res_id', '=', id), ('res_model', '=', model), ('res_field', '=', field)])
        if obj and obj.mimetype.startswith('image'):
            image_base64 = base64.b64decode(obj.datas)
            headers = [('Content-Type', obj.mimetype), ('Content-Length', obj.file_size)]
            return request.make_response(image_base64, headers)

        return werkzeug.utils.redirect(DEFAULT_IMG_URL, code=302)

    @http.route(['/web/image_weshop/<string:path>'], type='http', auth="public")
    def hash_image(self, path=None, **kwargs):
        if not path:
            return werkzeug.utils.redirect(DEFAULT_IMG_URL, code=302)
        store_fname = '{}/{}'.format(path[:2], path)
        _logger.info('>>> store_fname %s', store_fname)
        obj = request.env['ir.attachment'].sudo().search([('store_fname', '=', store_fname)], limit=1)
        _logger.info('>>> attachment obj %s', obj)
        if obj and obj.mimetype.startswith('image') and obj.res_model in ['product.template', 'product.image', 'ir.ui.view']:
            image_base64 = base64.b64decode(obj.datas)
            headers = [('Content-Type', obj.mimetype), ('Content-Length', obj.file_size)]
            return request.make_response(image_base64, headers)

        return werkzeug.utils.redirect(DEFAULT_IMG_URL, code=302)
