const wxpay = require('../../utils/pay.js')
const app = getApp()
const WXAPI = require('../../wxapi/main')
const shopCardUtils = require('../../utils/shopCartUtils.js')
var timer = require('../../utils/wxTimer.js')
Page({
  data: {
    statusType: ["待付款", "待发货", "待收货", "已取消", "已完成"],
    hasRefund: false,
    currentType: 0,
    wxTimerList: {},
    tabClass: ["", "", "", "", ""]
  },
  statusTap: function(e) {
    const curType = e.currentTarget.dataset.index;
    this.data.currentType = curType
    this.setData({
      currentType: curType
    });
    this.onShow();
  },
  refundApply: function(e) {
    // 申请售后
    const orderId = e.currentTarget.dataset.id;
    const amount = e.currentTarget.dataset.amount;
    wx.navigateTo({
      url: "/pages/order/refundApply?id=" + orderId + "&amount=" + amount
    })
  },
  orderDetail: function(e) {
    var orderId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: "/pages/order-details/index?id=" + orderId
    })
  },
  cancelOrderTap: function(e) {
    var that = this;
    var orderId = e.currentTarget.dataset.id;
    wx.showModal({
      title: '确定要取消该订单吗？',
      content: '',
      success: function(res) {
        if (res.confirm) {
          WXAPI.orderClose(orderId, wx.getStorageSync('token')).then(function(res) {
            if (res.code == 0) {
              that.onShow();
            }else{
              wx.showModal({
                title: '提示',
                content: res.msg,
                showCancel: false
              })
            }
          })
        }
      }
    })
  },
  toPayTap: function(e) {
    var that = this;
    var orderId = e.currentTarget.dataset.id;
    var money = e.currentTarget.dataset.money;
    var needScore = e.currentTarget.dataset.score;
    WXAPI.userAmount(wx.getStorageSync('token')).then(function(res) {
      if (res.code == 0) {
        // res.data.data.balance
        money = money - res.data.balance;
        var rate = res.data.payrate || 0;
        if (res.data.score < needScore) {
          wx.showModal({
            title: '错误',
            content: '您的积分不足，无法支付',
            showCancel: false
          })
          return;
        }
        if (money <= 0) {
          // 直接使用余额支付
          WXAPI.orderPay(orderId, wx.getStorageSync('token')).then(function(res) {
            that.onShow();
          })
        } else {
          let _fee = parseFloat((money * rate).toFixed(2));
          let _all = money + _fee;
          let _msg = '支付总额: ' + _all + '\r\n包含微信支付手续费: ' + _fee;
          wx.showModal({
            title: '请确认支付',
            content: _msg,
            confirmText: "确认支付",
            cancelText: "取消支付",
            success: function (res) {
              console.log(res);
              if (res.confirm) {
                wxpay.wxpay(app, _all, orderId, "/pages/order-list/index");
              } else {
                console.log('用户点击取消支付')
              }
            }
          });
        }
      } else {
        wx.showModal({
          title: '错误',
          content: '无法获取用户资金信息',
          showCancel: false
        })
      }
    })
  },
  onLoad: function(options) {
    if (options && options.type) {
      if (options.type == 99) {
        this.setData({
          hasRefund: true,
          currentType: options.type
        });
      } else {
        this.setData({
          hasRefund: false,
          currentType: options.type
        });
      }  
    }
  },
  onReady: function() {
    // 生命周期函数--监听页面初次渲染完成

  },
  getOrderStatistics: function() {
    var that = this;
    WXAPI.orderStatistics(wx.getStorageSync('token')).then(function(res) {
      if (res.code == 0) {
        var tabClass = that.data.tabClass;
        if (res.data.count_id_no_pay > 0) {
          tabClass[0] = "red-dot"
        } else {
          tabClass[0] = ""
        }
        if (res.data.count_id_no_transfer > 0) {
          tabClass[1] = "red-dot"
        } else {
          tabClass[1] = ""
        }
        if (res.data.count_id_no_confirm > 0) {
          tabClass[2] = "red-dot"
        } else {
          tabClass[2] = ""
        }
        if (res.data.count_id_no_reputation > 0) {
          tabClass[3] = "red-dot"
        } else {
          tabClass[3] = ""
        }
        if (res.data.count_id_success > 0) {
          //tabClass[4] = "red-dot"
        } else {
          //tabClass[4] = ""
        }

        that.setData({
          tabClass: tabClass,
        });
      }
    })
  },
  onShow: function() {
    // 获取订单列表
    var that = this;
    var postData = {
      token: wx.getStorageSync('token')
    };
    postData.hasRefund = that.data.hasRefund;
    if (!postData.hasRefund) {
      postData.status = that.data.currentType;
    }
    this.getOrderStatistics();
    WXAPI.orderList(postData).then(function(res) {
      if (res.code == 0) {
        that.setData({
          orderList: res.data.orderList,
          logisticsMap: res.data.logisticsMap,
          goodsMap: res.data.goodsMap
        });
        if (that.data.currentType==0){
          //初始化倒计时
          for (let i = 0; i < res.data.orderList.length; i++) {
            'use strict'
            let order = res.data.orderList[i];
            let s = order.dateAdd.replace(/-/g, "/");
            let d = new Date(s);
            let diff = d - new Date() + 30 * 60 * 1000;
            if (diff>0){
              diff = diff % (30 * 60 * 1000);
              diff = Math.ceil(diff / 1000)
              let minutes = Math.floor(diff / 60);
              let seconds = diff % 60;
              if (minutes<10){
                minutes = '0' + minutes;
              }
              let wxTimer = new timer({
                beginTime: "00:"+ minutes +":" + seconds,
                name: order.orderNumber,
                complete: function () {
                  wx.showModal({
                    title: '提示',
                    content: '订单' + order.orderNumber+'已超时关闭',
                    showCancel: false,
                    success: function (res) {
                      wx.reLaunch({ url: '/pages/my/index' })
                    }
                  })
                }
              })
              wxTimer.start(that);
            }
          }
        }
      } else {
        that.setData({
          orderList: null,
          logisticsMap: {},
          goodsMap: {}
        });
      }
    })
  },
  onHide: function() {
    // 生命周期函数--监听页面隐藏

  },
  onUnload: function() {
    // 生命周期函数--监听页面卸载

  },
  onPullDownRefresh: function() {
    // 页面相关事件处理函数--监听用户下拉动作

  },
  onReachBottom: function() {
    // 页面上拉触底事件的处理函数

  },

  addToShopCartFromOrder: function (e) {
    // 页面上拉触底事件的处理函数

    var orderId = e.currentTarget.dataset.id;
    var that = this;
    WXAPI.orderDetail(orderId, wx.getStorageSync('token')).then(function (res) {
      if (res.code != 0) {
        wx.showModal({
          title: '错误',
          content: res.msg,
          showCancel: false
        })
        return;
      }
      var orderDetail = res.data;
      if (orderDetail && orderDetail.goods && orderDetail.goods.length > 0) {
        var shopCarInfo = shopCardUtils.getShopCarInfo();
        const isDone = false;
        for (var i = 0; i < orderDetail.goods.length; i++) {
          const orderGood = orderDetail.goods[i];
          const goodsId = orderGood.goodsId;
          const goodsCount = orderDetail.goods.length;
          var count = 0;
          WXAPI.goodsDetail(goodsId).then(function (res) {
            if (res.data) {
              var goodDetail = shopCardUtils.buildShopCarItem(res.data);
              goodDetail.number = orderGood.number;
              count = count +1;

              if (orderGood.propertyChildIds) {
                WXAPI.goodsPrice({
                  goodsId: goodsId,
                  propertyChildIds: orderGood.propertyChildIds
                }).then(function (res) {
                  goodDetail.price = res.data.price;
                  goodDetail.score = res.data.score;
                  goodDetail.stores = res.data.stores;
                  goodDetail.propertyChildIds = orderGood.propertyChildIds;
                  goodDetail.label = orderGood.property;
                  that.updateAndRefreshShopCart(count, goodsCount, goodDetail, shopCarInfo);
                })
              } else { 
                that.updateAndRefreshShopCart(count, goodsCount, goodDetail, shopCarInfo);
              }
            }
          })
        } 
      } else {
        wx.showModal({
          title: '错误',
          content: "此订单没有可以回购的商品",
          showCancel: false
        })
        return;
      }
    })
  },

  updateAndRefreshShopCart: function (count, goodsCount, goodDetail, shopCarInfo) {
    shopCardUtils.addToShopCart(goodDetail, shopCarInfo);
    if (count === goodsCount) {
      wx.setStorage({
        key: 'shopCarInfo',
        data: shopCarInfo
      })
      wx.reLaunch({
        url: "/pages/shop-cart/index"
      });
    }

  },
})