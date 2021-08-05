# -*- coding: utf-8 -*-

import json
import base64

from odoo import http
from odoo.http import request

from .. import defs
from odoo.addons.oejia_weshop.controllers.base import BaseController

import logging

_logger = logging.getLogger(__name__)


class WxaQrcode(http.Controller, BaseController):
    pass
