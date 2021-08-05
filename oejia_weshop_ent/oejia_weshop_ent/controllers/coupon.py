# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta
import random
import logging

from odoo import http
from odoo.http import request

from odoo.addons.oejia_weshop.controllers.base import BaseController, dt_convert


_logger = logging.getLogger(__name__)


class WxappCoupon(http.Controller, BaseController):

    @http.route('/wxa/<string:sub_domain>/discounts/coupons', auth='public', methods=['GET', 'POST'], csrf=False)
    def coupons(self, sub_domain, type=None, **kwargs):
        try:
            ret, entry = self._check_domain(sub_domain)
            if ret:return ret

            data = []

            return self.res_err(700)

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, str(e))

    @http.route('/wxa/<string:sub_domain>/discounts/my', auth='public', methods=['GET', 'POST'], csrf=False)
    def my_coupons(self, sub_domain, type=None, **kwargs):
        try:
            ret, entry = self._check_domain(sub_domain)
            if ret:return ret

            data = []

            return self.res_err(700)

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, str(e))

