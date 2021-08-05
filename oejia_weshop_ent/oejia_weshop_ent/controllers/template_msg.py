# -*- coding: utf-8 -*-

import json

from odoo import http
from odoo.http import request

from .. import defs
from odoo.addons.oejia_weshop.controllers.base import BaseController

import logging

_logger = logging.getLogger(__name__)


class TemplateMsg(http.Controller, BaseController):

    @http.route('/wxa/<string:sub_domain>/template-msg/wxa/formId', auth='public', method=['POST'], csrf=False)
    def save_formid(self, sub_domain, token, formId=None, type=None, **kwargs):
        formid = formId
        ftype = type
        try:
            res, wechat_user, entry = self._check_user(sub_domain, token)
            if res:return res

            if not formid:
                return self.res_err(300)

            request.env['wxapp.formid'].sudo().create({
                'wechat_user_id': wechat_user.id,
                'formid': formid,
                'ftype': ftype,
            })
            return request.make_response(json.dumps({'code': 0, 'msg': 'success'}))

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, str(e))


    @http.route('/wxa/<string:sub_domain>/template-msg/put', auth='public', methods=['POST'], csrf=False, type='http')
    def send_template_msg(self, sub_domain, **kwargs):
        try:
            _logger.info('>>> kwargs: %s'%kwargs)
            token = kwargs.get('token', None)

            res, wechat_user, entry = self._check_user(sub_domain, token)
            if res:return res

            module = kwargs['module'] # immediately 立即发送模板消息；order 所属订单模块; comment 留言评论模块； cmsnews 文章投稿模块；saleDistributionApply 分销商申请
            template_id = kwargs['template_id']
            postJsonString = kwargs['postJsonString']
            postJson = json.loads(postJsonString)
            type = kwargs['type'] # 0 小程序 1 服务号

            business_id = kwargs.get('business_id', None) # module不为immediately时必填，代表对应的【订单/留言/文章/分销申请】ID
            trigger = kwargs.get('trigger', None) # module不为immediately时必填，代表触发的状态

            form_id = kwargs.get('form_id', None) # type=0 小程序
            url = kwargs.get('url', None) # type=0 小程序
            emphasis_keyword = kwargs.get('emphasis_keyword', None) # type=0 小程序

            if template_id=='uJL7D8ZWZfO29Blfq34YbuKitusY6QXxJHMuhQm_lco':
                # 确认收货后立马通知客户评论商品
                return self.res_ok()
            if template_id=='uJL7D8ZWZfO29Blfq34YbuKitusY6QXxJHMuhQm_lco':
                # 评论后立马反馈结果给客户
                return self.res_ok()
            if template_id=='mGVFc31MYNMoR9Z-A9yeVVYLIVGphUVcK2-S2UdZHmg':
                # 创建订单后半个小时自动关闭订单的通知
                return self.res_ok()
            if template_id=='Arm2aS1rsklRuJSrfz-QVoyUzLVmU2vEMn_HgMxuegw':
                # 创建订单发货后通知用户
                return self.res_ok()

            #from wechatpy.client import WeChatClient
            #client = WeChatClient(entry.app_id, entry.secret)

            #if trigger=='2':
            #    template_id = 'qu0K6anpozZNj3uf1gcyyOFZSbM8ZKDTrk_TI0IScXg' #新订单通知
            #else:
            #    template_id = 'ByIUs56ntvPpQ12GeWDLMr_0fQHdVnZz83-LnEkBZUg' #订单取消通知
            #client.wxa.send_template_message(wechat_user.open_id, template_id, postJson, form_id, url)

            return self.res_ok()

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, str(e))
