// pages/bind-login/index.js
var app = getApp()
const WXAPI = require('../../wxapi/main')
Page({

  /**
   * 页面的初始数据
   */
  data: {
  
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
  
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
  
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
  
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
  
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
  
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
  
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
  
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
  
  },

  bindCancel: function () {
    wx.navigateBack({})
  },
  register_and_bind: function (registerData) {
    // 下面开始调用注册接口
    wx.showLoading();
    WXAPI.register(registerData).then(function (res) {
      wx.hideLoading();
      wx.removeStorageSync('registerData');
      if (res.code != 0) {
        var title = res.code == -2 ? '提示' : '错误';
        wx.showModal({
          title: title,
          content: res.msg,
          showCancel: false,
          success(res) {
            if (res.confirm) {
              wx.navigateBack({});
            }
          }
        })
        return;
      }else{
        // 成功注册并绑定后自动执行登录请求
        wx.login({
          success: function (res) {
            wx.showLoading();
            WXAPI.login(res.code).then(function (res) {
              if (res.code != 0) {
                // 登录错误
                wx.hideLoading();
                wx.showModal({
                  title: '提示',
                  content: '无法登录，请重试',
                  showCancel: false
                })
                return;
              }
              wx.setStorageSync('token', res.data.token)
              wx.setStorageSync('uid', res.data.uid)
              wx.setStorageSync('userid', res.data.info.base.userid)
              // 回到原来的地方放
              app.navigateToLogin = false
              app.bindChanged = true
              wx.reLaunch({ url: '/pages/index/index' })
              //wx.navigateBack({ delta: 2 });
            })
          }
        })
      }
    })
  },
  bindSave: function (e) {
    var that = this;
    
    var loginToken = wx.getStorageSync('token')
    var username = e.detail.value.username;
    var password = e.detail.value.password;

    if (!username || !password) {
      wx.showModal({
        title: '错误',
        content: '请填写完整',
        showCancel: false
      })
      return
    }

    var postData = {
      token: loginToken,
      username: username,
      password: password
    }

    let registerData = wx.getStorageSync('registerData');
    if (registerData){
      registerData.username = username;
      registerData.password = password;
      return that.register_and_bind(registerData)
    }

    wx.showLoading();
    WXAPI.request('/user/bind/login', true, 'post', postData).then(function (res) {
      wx.hideLoading();
      if (res.code == 0) {
        wx.setStorageSync('userid', res.data.userid);
        app.bindChanged = true;
        wx.reLaunch({ url: '/pages/index/index' });
        //wx.navigateBack({});
        wx.showToast({
          title: '绑定成功',
          icon: 'none',
        });
      } else {
        var title = res.code == -2 ? '提示' : '错误';
        wx.showModal({
          title: title,
          content: res.msg,
          showCancel: false
        })
      }
    })
  }
})