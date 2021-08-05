# -*- coding: utf-8 -*-

import time

from odoo import models, fields, api, exceptions


class WxappMsgTpl(models.Model):

    _name = 'wxapp.msg.tpl'
    _description = u'消息模板配置'

    tpl_id = fields.Char('模板ID')
    tpl_content = fields.Char('模板内容(将小程序后台对应内容的key按顺序用逗号分隔填入)')


    @api.model
    def get_keys(self, tpl_id, length):
        obj = self.search([('tpl_id', '=', tpl_id)])
        if obj:
            if obj.tpl_content:
                _val = obj.tpl_content.replace(u'，', ',')
                _val_list = _val.split(',')
                _val_list = [e for e in _val_list if e]
                if len(_val_list)>=length:
                    return _val_list
        return [None] * length
