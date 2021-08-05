# -*- coding: utf-8 -*-

from odoo.addons.oejia_weshop.const import Const


class PaymentStatus(Const):
    unpaid = ('unpaid', '未支付')
    success = ('success', '成功')
    fail = ('fail', '失败')



class LogisticsValuationType(Const):
    #by_piece = ('by_piece', u'按件')
    #by_weight = ('by_weight', u'按重量')
    by_amount = ('by_amount', u'按订单金额')

class LogisticsValuationResponseType(Const):
    by_piece = ('by_piece', 0)
    by_weight = ('by_weight', 1)
    by_amount = ('by_amount', 3)

class LogisticsValuationRequestType(Const):
    by_piece = (0, 'by_piece')
    by_weight = (1, 'by_weight')
    by_amount = (3, 'by_amount')

class TransportationUnit(Const):
    by_piece = ('by_piece', u'件')
    by_weight = ('by_weight', u'KG')
    by_amount = ('by_amount', u'元')


class TransportType(Const):
    express = ('express', u'快递配送或商家配送')

class TransportResponseType(Const):
    express = ('express', 0)
    ems = ('ems', 1)
    post = ('post', 2)
    by_self = ('self', 3)

class TransportRequestType(Const):
    express = (0, 'express')
    ems = (1, 'ems')
    post = (2, 'post')
    by_self = (3, 'self')

class FormType(Const):
    form = ('form', 'form')
    pay = ('pay', 'pay')

class ScoreLogType(Const):
    default = ('default', u'默认')
    admin = ('admin', u'管理员调整')
    consume = ('consume', u'消费返')
    deduct = ('deduct', u'消费抵扣')
    sign = ('sign', u'签到奖励')

class BalanceLogType(Const):
    default = ('default', u'默认')
    admin = ('admin', u'管理员调整')
    orderpay = ('orderpay', u'买单支付')

class OrderResponseState(Const):
    draft = ('draft', 0)
    sent = ('sent', 1)
    sale = ('sale', 2)
    done = ('done', 3)
    cancel = ('cancel', 4)

class RefundStatus(Const):
    pending = ('0', '待处理')
    cancelled = ('1', '已撤回')
    refused = ('2', '本次申请已拒绝')
    doing = ('3', '处理中')
    completed = ('4', '处理完成')
