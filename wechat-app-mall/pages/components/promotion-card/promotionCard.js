// pages/components/promotion-card.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    goodsList:{
      type: Array
    },
    promotionType:{
      type: String
    },
    time:{
      type: String
    },
    promotionId:{
      type: Number
    },
    startTime:{
      type:Number,
      observer: '_startTime'
    },
    endTime:{
      type:Number,
      observer: '_endTime'
    },
    timeStr:{
      type: String
    }
  },

  data: {
    hasToken: false,
    promotionType: 'Being',
    goodsList:[],
    promotionId: 0,
    endTime: 0,
    startTime: 0,
    timeStr: '',
    day:'',
    hour:'',
    min: '',
    sec: ''
  },

  /**
   * 组件的方法列表
   */
  methods: {
    toDetailsTap: function (e) {
      wx.navigateTo({
        url: "/pages/goods-details/index?id=" + e.currentTarget.dataset.id + '&promotionId=' + e.currentTarget.dataset.promotionid + '&promotionType=' + e.currentTarget.dataset.promotiontype
      })
    },
    toPromotionList: function (e) {
      wx.navigateTo({
        url: "/pages/promotion-list/index?promotionId=" + e.currentTarget.dataset.promotionid
      })
    },
    countDown: function (timestamp){
      const that = this
      var cd = setInterval(function () {
        var nowTime = new Date();
        var endTime = new Date(timestamp * 1000);
        var t = endTime.getTime() - nowTime.getTime();
        var day = Math.floor(t/1000/60/60/24);
        var hour = Math.floor(t / 1000 / 60 / 60 % 24);
        var min = Math.floor(t / 1000 / 60 % 60);
        var sec = Math.floor(t / 1000 % 60);
        if (t<=0){
          // 如果倒计时结束调用父类刷新方法更新
          day = hour = min = sec = 0
          that.triggerEvent('refresh')
          clearInterval(cd);
        }
        if (hour < 10) {
          hour = "0" + hour;
        }
        else if (hour < 0) {
          hour = ''
        }
        if (min < 10) {
          min = "0" + min;
        }
        else if (min < 0) {
          min = ''
        }
        if (sec < 10) {
          sec = "0" + sec;
        }
        else if(sec<0){
          sec = ''
        }
        that.setData({
          day,
          hour,
          min,
          sec
        })
      }, 1000);
    },
    beginCountDown: function(){
      var nowTime = parseInt(new Date().getTime() / 1000);
      var startTime = this.data.startTime;
      var endTime = this.data.endTime;
      var promotionType = ''
      if (nowTime < startTime) {
        promotionType = 'Advance'
        // 时间戳转标准时间
        var st = new Date(startTime * 1000)
        var year = st.getFullYear();
        var month = st.getMonth() + 1;
        var date = st.getDate();
        var hour = st.getHours();
        var minute = st.getMinutes();
        var second = st.getSeconds();
        var timeStr = month + "月" + date + "日" + hour + "点" + minute + ":" + second;
        var timeStr = month + "月" + date + "日" + hour + "点"
        if (minute && !second) {
          timeStr += (minute + '分')
        }
        if (second) {
          timeStr += (minute + '分' + second + '秒')
        }
      }
      else if (nowTime > startTime && nowTime < endTime) {
        promotionType = 'Being'
        this.countDown(endTime)
      }
      this.setData({
        promotionType,
        timeStr
      })
    },
    _endTime: function (newVal, oldVal) {
      const that = this 
      that.beginCountDown()
    },
    _startTime: function () {
      const that = this
      that.beginCountDown()
    }
  },
 lifetimes: {
    attached: function() { 
      let token = wx.getStorageSync('userid');
      if (token) {
        this.setData({
          hasToken: true
        })
      }
      this.beginCountDown()
    }
  }
})
