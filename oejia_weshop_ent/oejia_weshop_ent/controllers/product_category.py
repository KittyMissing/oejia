# -*- coding: utf-8 -*-

import json

from odoo import http
from odoo.http import request

from odoo.addons.oejia_weshop.controllers.product_category import WxappCategory


import logging

_logger = logging.getLogger(__name__)


class WxappCategoryExt(WxappCategory):

    @http.route('/wxa/<string:sub_domain>/shop/goods/category/nav', auth='public', methods=['GET'])
    def nav(self, sub_domain,  **kwargs):
        fm = kwargs.get('fm', None)
        ret, entry = self._check_domain(sub_domain)
        if ret:return ret

        try:
            all_category = request.env['wxapp.product.category'].sudo().search([
                ('is_use', '=', True),
                #('level', 'in', [0, 1, 2]),
            ], order='level')
            if not all_category:
                return self.res_err(404)

            data = {}
            for category in all_category:
                _logger.info('>>> category %s %s', category.name, category)
                _id = category.id
                _pid = category.pid.id if category.pid else 0
                if category.level==0:
                    info = {
                        'id': _id,
                        'pid': _pid,
                        'name': category.name,
                        'childs': {},
                        'icon': category.get_icon_image(),
                        'path': [_id],
                    }
                    data[_id] = info
                    info['path_display'] = category.name
                elif category.level==1:
                    info = {
                        'id': _id,
                        'pid': _pid,
                        'name': category.name,
                        'childs': {},
                        'childs_len': 0,
                        'icon': category.get_icon_image(),
                        'path': [_pid, _id],
                    }
                    if _pid in data:
                        data[_pid]['childs'][_id] = info
                        info['path_display'] = '%s / %s'%(data[_pid]['path_display'], category.name)
                elif category.level==2:
                    _pid_pid = category.pid.pid.id
                    info = {
                        'id': _id,
                        'pid': _pid,
                        'name': category.name,
                        'childs': {},
                        'icon': category.get_icon_image(),
                        'path': [_pid_pid, _pid, _id],
                    }
                    if _pid_pid in data:
                        if _pid in data[_pid_pid]['childs']:
                            data[_pid_pid]['childs'][_pid]['childs'][_id] = info
                            data[_pid_pid]['childs'][_pid]['childs_len'] += 1
                            info['path_display'] = '%s / %s'%(data[_pid_pid]['childs'][_pid]['path_display'] , category.name)
            for fst in data.values():
                _no_child = []
                for sec in fst['childs'].values():
                    if sec['childs_len']==0:
                        _no_child.append(sec)
                for _sec in _no_child:
                    del fst['childs'][_sec['id']]
                if _no_child:
                    fst['childs'][0] = {
                        'id': fst['id'],
                        'pid': fst['id'],
                        'name': '分类',
                        'childs':{ sec['id']:sec for sec in _no_child},
                        'icon': '',
                        'path': [fst['id'], fst['id']],
                        'path_display': fst['name'],
                    }
            if fm=='pc':
                return self.res_ok(list(data.values()))
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            p_data = {
                'id': 0,
                'pid': 0,
                'name': '全部',
                'childs': {
                    0: {
                        'id': 0,
                        'pid': 0,
                        'name': '全部分类',
                        'childs': {
                            0: {
                                'id': 0,
                                'pid': 0,
                                'name': '全部',
                                'childs': {},
                                'icon': base_url + '/oejia_weshop_ent/static/src/img/all.jpg',
                                'path': [0],
                                'path_display': '全部',
                            }
                        },
                        'childs_len': 1,
                    }
                },
            }
            _logger.info(data)
            for fst_id in data.keys():
                _data = data[fst_id]
                _logger.info('>>> for %s', _data)
                p_data['childs'][0]['childs'][fst_id] = {
                    'id': _data['id'],
                    'pid': _data['pid'],
                    'name': _data['name'],
                    'childs': {},
                    'icon': _data['icon'],
                    'path': [fst_id],
                    'path_display': _data['path_display'],
                }
                p_data['childs'][0]['childs_len'] += 1

                p_data['childs'][fst_id] = {
                    'id': fst_id,
                    'pid': _data['pid'],
                    'name': _data['name'],
                    'childs': {},
                    'childs_len': 0,
                    'icon': _data['icon']
                }
                for sec_id in _data['childs'].keys():
                    if sec_id==0:
                        continue
                    s_data = _data['childs'][sec_id]
                    _logger.info('>>> sec for %s', s_data)
                    p_data['childs'][fst_id]['childs'][sec_id] = {
                        'id': s_data['id'],
                        'pid': s_data['pid'],
                        'name':s_data['name'],
                        'childs': {},
                        'icon': s_data['icon'],
                        'path': [fst_id, sec_id],
                        'path_display': s_data['path_display'],
                    }
                    p_data['childs'][fst_id]['childs_len'] += 1
            ret_data = list(data.values())
            ret_data.insert(0, p_data)

            return self.res_ok(ret_data)

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, str(e))
