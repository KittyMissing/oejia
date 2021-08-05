# -*- coding: utf-8 -*-

import json
from datetime import datetime
import pytz

from odoo import http
from odoo.http import request
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import fields

from .. import defs
from odoo.addons.oejia_weshop.controllers.base import BaseController, dt_convert

import logging

_logger = logging.getLogger(__name__)


class WxappScore(http.Controller, BaseController):


    @http.route('/wxa/<string:sub_domain>/score/logs', auth='public', methods=['GET', 'POST'], csrf=False)
    def score_logs(self, sub_domain, token=None, page=1, pageSize=20, **kwargs):
        page = int(page)
        pageSize = int(pageSize)
        try:
            res, wechat_user, entry = self._check_user(sub_domain, token)
            if res:return res


            objs = request.env['oe.score.logs'].sudo().search([('partner_id', '=', wechat_user.partner_id.id)], offset=(page-1)*pageSize, limit=pageSize, order="id desc")
            _data = {
                'result':[{
                    'typeStr': obj.log_type_show(),
                    'remark': obj.remark,
                    'score': obj.score,
                    'behavior': int(obj.behavior),
                    'dateAdd': dt_convert(obj.create_date),
                } for obj in objs],
            }
            return self.res_ok(_data)

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, str(e))

