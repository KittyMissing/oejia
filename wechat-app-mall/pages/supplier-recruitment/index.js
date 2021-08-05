// pages/supplier-recruitment/index.js
import WxValidate from '../../utils/WxValidate.js'
const WXAPI = require('../../wxapi/main')
Page({

  /**
   * 页面的初始数据
   */
  data: {
    sampleImages: [],
    cardImages: [],
    form: {
      companyName: '',
      address: '',
      contact: '',
      phone: '',
      description: ''
    }
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    this.initValidate();
  },

  initValidate() {
    const rules = {
      companyName: {
        required: true,
        maxlength: 100
      },
      address: {
        required: true,
      },
      contact: {
        required: true,
      },
      phone: {
        required: true,
        tel: true
      },
      description: {
        required: true,
      }
    }
    const messages = {
      companyName: {
        required: '请填写公司名称'
      },
      address: {
        required: '请填写联系地址'
      },
      contact: {
        required: '请填写联系人'
      },
      phone: {
        required: '请填写联系电话'
      },
      description: {
        required: '请填写特点自述'
      }
    }
    this.WxValidate = new WxValidate(rules, messages)
  },

  submitSupplierInfo: function(e) {
    //校验表单
    var params = e.detail.value
    if (!this.WxValidate.checkForm(params)) {
      const error = this.WxValidate.errorList[0];
      this.showModal(error);
      return false;
    }
    params.token = wx.getStorageSync('token');
    this.createSupplierRecruitment(params);
  },

  createSupplierRecruitment: function(data) {
    var that = this;
    WXAPI.createSupplierRecruitment(data).then(function(res) {
      if (res.code != 0) {
        var title = res.code == -2 ? '提示' : '错误';
        wx.showModal({
          title: title,
          showCancel: false,
        })
        return;
      } else {
        // 开始并行上传图片
        const promiseList = that.getPromiseList(res.data);
        const result = Promise.all(promiseList).then((res) => {

          return res;
        }).catch((error) => {
          console.log(error);
        });

        wx.showModal({
          title: "提交成功",
          showCancel: false,
          success(res) {
            if (res.confirm) {
              wx.navigateBack({});
            }
          }
        })
      }
    })
  },

  getPromiseList: function (postID) {
    // 将选择的图片组成一个Promise数组，准备进行并行上传
    var images = this.data.sampleImages.concat(this.data.cardImages);
    const promiseList = images.map(path => {
      return new Promise(resolve => {
        wx.uploadFile({
          url: WXAPI.URL_PRE + '/supplier/upload?token=' + wx.getStorageSync('token') + '&id='+ postID,
          filePath: path,
          name: 'images',
          success: (res) => {
            const data = res.data;
            resolve(data);
          }
        });
      });
    })

    return promiseList;
  },

  showModal: function(error) {
    wx.showModal({
      content: error.msg,
      showCancel: false,
    })
  },

  handleImagePreview: function(e) {
    const idx = e.target.dataset.idx
    const images = this.data.images
    wx.previewImage({
      current: images[idx], //当前预览的图片
      urls: images, //所有要预览的图片
    })
  },

  removeImage: function(e) {
    const type = e.target.dataset.type;
    const index = e.target.dataset.index;
    if (type === "cardImages") {
      this.data.cardImages.splice(index, 1);
      this.setData({
        cardImages: this.data.cardImages
      });
    } else {
      this.data.sampleImages.splice(index, 1);
      this.setData({
        sampleImages: this.data.sampleImages
      });
    }

  },

  uploadImage: function(event) {
    var type = event.currentTarget.dataset.id;
    var that = this;
    wx.chooseImage({
      count: 8,
      sizeType: ['original', 'compressed'],
      sourceType: ['album', 'camera'],
      success: function(res) {
        const tempFilePaths = res.tempFilePaths;
        console.log(tempFilePaths);
        var sampleImages = that.data.sampleImages;
        var cardImages = that.data.cardImages;

        if (type === "sampleImages") {
          sampleImages = sampleImages.concat(tempFilePaths);
          if (sampleImages.length > 8) {
            wx.showModal({
              content: "最多上传8张图片",
              showCancel: false,
            })
            return;
          }
          that.setData({
            sampleImages: sampleImages
          });
        } else {
          cardImages = cardImages.concat(tempFilePaths);
          if (cardImages.length > 1) {
            wx.showModal({
              content: "最多上传1张图片",
              showCancel: false,
            })
            return;
          }
          that.setData({
            cardImages: cardImages
          });
        }
      },
    })
  }
})