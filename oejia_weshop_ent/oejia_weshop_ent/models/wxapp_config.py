# coding=utf-8
import logging
import json

from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class WxappConfig(models.Model):

    _inherit = 'wxapp.config'

    wechat_pay_id = fields.Char('微信支付商户号')
    wechat_pay_secret = fields.Char('微信支付商户秘钥')
    sub_mch_id = fields.Char('微信支付特约商户号') #特约商户号

    msgtpl_order_created = fields.Char('下单成功通知')
    msgtpl_order_paid = fields.Char('订单支付成功通知')
    msgtpl_order_delivery = fields.Char('订单发货通知')
    msgtpl_order_closed = fields.Char('订单已关闭通知')
    msgtpl_order_confirmed = fields.Char('订单已确认待付款通知')

    user_id = fields.Many2one('res.users', string='默认销售员')

    enable_no_service_period = fields.Boolean('启用禁止下单时段', default=False)
    no_service_start_hour = fields.Integer('禁止下单开始时间小时(0-23)')
    no_service_start_minute = fields.Integer('禁止下单开始时间分(0-59)')
    no_service_long = fields.Integer('禁止下单持续时长/分钟')
    auto_cancel_expired_order= fields.Boolean('超时未支付订单自动取消', default=False)

    recharge_open = fields.Boolean('是否开启钱包、积分', default=False)

    @api.multi
    def restore_attr_val_str(self):
        self.env['product.product'].search([])._compute_attr_val_str()

    def _register_hook(self):
        super(WxappConfig, self)._register_hook()
        pass

    def get_config(self, key):
        if key == 'RECHARGE_OPEN':
            key = 'recharge_open'
        if key == 'msgtpl_id_list':
            ret = []
            for k in dir(self):
                if k.startswith('msgtpl_order') and getattr(self, k):
                    ret.append(getattr(self, k))
            return ret
        return super(WxappConfig, self).get_config(key)

    def sync_msgtpl(self):
        to_do = [1885, 5553, 11130, 2414, 1569]#[self.msgtpl_order_created, self.msgtpl_order_paid, self.msgtpl_order_delivery, self.msgtpl_order_closed, self.msgtpl_order_confirmed]
        for tpl_id in to_do:
            if tpl_id:
                self.get_msgtpl_content(tpl_id)

    def get_msgtpl_content(self, tpl_id):
        from wechatpy.client import WeChatClient
        client = WeChatClient(self.app_id, self.secret)
        try:
            res = client.wxa._get('wxaapi/newtmpl/getpubtemplatekeywords', params={'tid': tpl_id})
            if res['errcode']==0:
                M = self.env['wxapp.msg.tpl'].sudo()
                obj = M.search([('tpl_id', '=', tpl_id)])
                if obj:
                    obj.write({'tpl_content': json.dumps(res['data'])})
                else:
                    M.create({'tpl_id': tpl_id, 'tpl_content': json.dumps(res['data'])})
        except:
            import traceback;traceback.print_exc()

    def restore_product_img_url(self):
        all_product = self.env['product.template'].search([])
        all_product._get_main_image()
        all_product._get_multi_images()

    def get_ext_config(self):
        ret = super(WxappConfig, self).get_ext_config()
        return ret
