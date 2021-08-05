# -*- coding: utf-8 -*-

import json
import logging

import odoo
from odoo import http
from odoo.http import request

from odoo.addons.oejia_weshop.controllers.user import WxappUser
from odoo.addons.oejia_weshop.controllers.base import BaseController, dt_convert


_logger = logging.getLogger(__name__)


class WxappUsertExt(WxappUser):

    def get_user_info(self, wechat_user):
        ret = super(WxappUsertExt, self).get_user_info(wechat_user)
        user = wechat_user.user_id
        ret['base']['username'] = user and user.login or ''
        ret['base']['nickname'] = user and user.name or ''
        ret['base']['avatar'] = wechat_user.avatar_url or ''
        ret['base']['userid'] = user and user.id or ''
        ret['base']['vat'] = wechat_user.vat or ''
        return ret

    def user_auth(self, username, password):
        # 账号验证
        _code = -1
        _error = u'登录异常'
        old_uid = request.uid
        try:
            uid = request.session.authenticate(request.session.db, username, password)
            return 0, uid
        except odoo.exceptions.AccessDenied as e:
            request.uid = old_uid
            if e.args == odoo.exceptions.AccessDenied().args:
                _error = u'用户名或密码不正确'
                _code = -2
            else:
                _error = e.args[0]
                _code = -99
            _logger.info('>>> %s %s', _code, _error)
            return _code, _error

    @http.route('/wxa/<string:sub_domain>/user/bind/login', auth='public', methods=['POST'], csrf=False, type='http')
    def bind(self, sub_domain, **kwargs):
        # 绑定系统账号
        try:
            token = kwargs.get('token', None)

            res, wechat_user, entry = self._check_user(sub_domain, token)
            if res:return res

            username = kwargs.get('username', None)
            password = kwargs.get('password', None)

            _code, ret = self.user_auth(username, password)
            if _code==0:
                request.session['login_uid'] = ret
                _logger.info('>>> set session login_uid %s', ret)
                wechat_user.write({
                    'user_id': ret,
                    'partner_id': request.env['res.users'].sudo().browse(ret).partner_id.id,
                    'category_id': [(4, request.env.ref('oejia_weshop.res_partner_category_data_1').sudo().id)],
                })
                return self.res_ok({'userid': ret})
            else:
                return self.res_err(_code, ret)
        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, '服务异常')

    @http.route()
    def register(self, *args, **kwargs):
        if kwargs.get('username'):
            # 注册的同时绑定系统账号
            _code, ret = self.user_auth(kwargs.get('username'), kwargs.get('password'))
            if _code==0:
                request.user_id = ret
            else:
                return self.res_err(_code, ret)
        return super(WxappUsertExt, self).register(*args, **kwargs)

