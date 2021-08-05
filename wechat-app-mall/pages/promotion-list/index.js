// pages/promotion-list/promotion-list.js
const WXAPI = require('../../wxapi/main')
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    hasToken: false,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let token = wx.getStorageSync('userid');
    if (token) {
      this.setData({
        hasToken: true
      })
    }
    const that = this
    if(options.promotionId){
      WXAPI.promotionDetail(options.promotionId).then(function(res){
        that.setData({
          goodsList: res.data.goodsList,
          startTime: res.data.startTime,
          startTimeStr: res.data.startTimeStr,
          endTime: res.data.endTime,
          endTimeStr: res.data.endTimeStr,
          activityType: res.data.activityType,
          partnerType: res.data.partnerType,
          promotionType: res.data.promotionType,
          promotionId: res.data.promotionId,
        })
      })
    }
  },

  toDetailsTap: function (e) {
    wx.navigateTo({
      url: "/pages/goods-details/index?id=" + e.currentTarget.dataset.id + '&promotionId=' + e.currentTarget.dataset.promotionid + '&promotionType=' + e.currentTarget.dataset.promotiontype
    })
  },
})