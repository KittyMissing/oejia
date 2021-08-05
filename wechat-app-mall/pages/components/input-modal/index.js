// pages/components/input-modal/index.js
Component({
  properties: {
    buyNum: {
      type: Number
    }
  },
  /**
   * 页面的初始数据
   */
  data: {
    buyNum: 0
  },
  methods: {
    cancelBuyNum: function() {
      this.triggerEvent("cancelBuyNum");
    },

    confirmBuyNum: function(e) {
      var data = {
        number: this.data.buyNum
      };
      this.triggerEvent("confirmBuyNum", data);
    },
    setBuyNum: function(e) {
      this.setData({
        buyNum: e.detail.value
      });
    },
    jianBtnTap: function() {
      this.setData({
        buyNum: this.data.buyNum - 1
      });
    },
    jiaBtnTap: function() {
      this.setData({
        buyNum: this.data.buyNum + 1
      });
    }
  }
})