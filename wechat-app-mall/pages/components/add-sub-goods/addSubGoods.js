const WXAPI = require('../../../wxapi/main')
var app = getApp();
Component({
  properties: {
    goodsId: {
      type: String
    },
    goodsDetail: {
      type: Object
    },
    buyNum: {
      type:Number
    },
    stores: {
      type: Number
    }
  },
  data: {
    showInputModal: false,
    buyNum: 0,
    stores: 0,
    totalPrice: 0,
    totalScore: 0
  },
  methods: {
    tapAddGoods: function(e) {
      if (this.data.showInputModal)return false;
      var number = e.detail.number;
      var buyNum = number || (this.data.buyNum + 1);
      var goodsDetail = this.properties.goodsDetail;
      var stores = this.properties.stores;
      var goodsId = this.properties.goodsId;;
      let that = this;

      WXAPI.goodsDetail(goodsId).then(function (res) {
        //有规格选择
        if (res.data.properties && res.data.properties.length > 0) {
          that.toDetailsTap(goodsId, false);
        } else { // 没有规格选择
          stores = res.data.basicInfo.stores;
          that.setData({
            goodsStore: stores
          });

          if (buyNum > stores) {
            wx.showModal({
              title: '提示',
              content: res.data.basicInfo.name + ' 库存不足，请重新购买',
              showCancel: false,
              duration: 200
            });
            return;
          }
          //更新购物车信息
          that.updateShopCarInfo(res.data, buyNum - that.data.buyNum);
        }
      });
    },
    tapNumEdit: function(e) {
      this.setData({
        showInputModal: true
      });
    },
    onCancelBuyNum:function(){
      this.setData({
        showInputModal: false
      });
    },
  
    onConfirmBuyNum: function (e) {
      if (e.detail.number<1){
        wx.showModal({
          title: '提示',
          content: '请输入合法的数字',
          showCancel: false
        })
      }else{
        this.setData({
          showInputModal: false
        });
        this.tapAddGoods(e)
      }
    },

    toDetailsTap: function (goodsId, hideShopPopup) {
      wx.navigateTo({
        url: "/pages/goods-details/index?id=" + goodsId + "&hideShopPopup=" + hideShopPopup
      })
    },

    subGoods: function(e) {
      var shopCarInfo = wx.getStorageSync('shopCarInfo');
      if (shopCarInfo && shopCarInfo.shopList && shopCarInfo.shopList.length > 0) {
        for (var i = 0; i < shopCarInfo.shopList.length; i++) {
          var tmpShopCarMap = shopCarInfo.shopList[i];
          if (tmpShopCarMap.goodsId == this.properties.goodsId) {
            tmpShopCarMap.number = tmpShopCarMap.number - 1;
            if (tmpShopCarMap.number === 0) {
              tmpShopCarMap.active = false;
              shopCarInfo.shopList.splice(i, 1);
            }
            shopCarInfo.totalPrice = shopCarInfo.totalPrice - parseFloat(tmpShopCarMap.price);
            shopCarInfo.totalScore = shopCarInfo.totalScore - tmpShopCarMap.score;
            shopCarInfo.shopNum = shopCarInfo.shopNum - 1
            break;
          }
        }
      }
      shopCarInfo.totalPrice = parseFloat(shopCarInfo.totalPrice.toFixed(2));
      wx.setStorageSync("shopCarInfo", shopCarInfo);
      this.setData({
        buyNum: this.data.buyNum - 1
      });
      var data = {
        totalPrice: shopCarInfo.totalPrice,
        totalScore: shopCarInfo.totalScore,
        shopNum: shopCarInfo.shopNum
      };
      this.triggerEvent("totalPriceChange", data);
    },

    /**
     * 更新购物车信息
     */
    updateShopCarInfo: function(goodsDetail, plus) {
      // 加入购物车
      var shopGood = this.getShopGoodInfo(goodsDetail, plus);
      var shopCarInfo = this.getShopCarInfo();
      this.updateShopList(shopCarInfo.shopList, shopGood);

      // 计算购物车总件数， 总价格， 总积分
      shopCarInfo.shopNum = shopCarInfo.shopNum + plus;
      shopCarInfo.totalPrice = shopCarInfo.totalPrice + parseFloat(shopGood.price * plus);
      shopCarInfo.totalScore = shopCarInfo.totalScore + shopGood.score * plus;

      shopCarInfo.totalPrice = parseFloat(shopCarInfo.totalPrice.toFixed(2));
      //shopCarInfo.kjId = this.data.kjId;
      wx.setStorage({
        key: 'shopCarInfo',
        data: shopCarInfo
      })

      this.setData({
        buyNum: this.data.buyNum + plus,
        totalPrice: shopCarInfo.totalPrice,
        totalScore: shopCarInfo.totalScore,
        shopNum: shopCarInfo.shopNum
      });

      var data = {
        totalPrice: shopCarInfo.totalPrice,
        totalScore: shopCarInfo.totalScore,
        shopNum: shopCarInfo.shopNum
      };
      this.triggerEvent("totalPriceChange", data);
    },

    updateShopList: function(shopList, shopCarMap) {
      if (shopList.length === 0) {
        shopList.push(shopCarMap);
        return;
      }

      var hasSameGoodsIndex = -1;
      for (var i = 0; i < shopList.length; i++) {
        var tmpShopCarMap = shopList[i];
        if (tmpShopCarMap.goodsId == shopCarMap.goodsId && (!tmpShopCarMap.propertyChildIds ||tmpShopCarMap.propertyChildIds == shopCarMap.propertyChildIds)){
          hasSameGoodsIndex = i;
          shopCarMap.number = shopCarMap.number + tmpShopCarMap.number;
          break;
        }
      }

      if (hasSameGoodsIndex > -1) {
        shopList.splice(hasSameGoodsIndex, 1, shopCarMap);
      } else {
        shopList.push(shopCarMap);
      }
    },

    getShopCarInfo: function() {
      var shopCarInfo = wx.getStorageSync('shopCarInfo');

      if (!shopCarInfo || shopCarInfo === ""){
        shopCarInfo = {};
      }
      
      if (!shopCarInfo.shopList) {
        shopCarInfo.shopList = [];
      }

      if (!shopCarInfo.totalPrice) {
        shopCarInfo.totalPrice = 0;
      }

      if (!shopCarInfo.shopNum) {
        shopCarInfo.shopNum = 0;
      }

      if (!shopCarInfo.totalScore) {
        shopCarInfo.totalScore = 0;
      }

      return shopCarInfo;
    },

    getShopGoodInfo: function(goodsDetail, plus) {
      return {
        goodsId: goodsDetail.basicInfo.id,
        pic: goodsDetail.basicInfo.pic, // 产品图片url
        name: goodsDetail.basicInfo.name,
        propertyChildIds: "", //产品规格信息
        label: "", //产品规格名称
        price: goodsDetail.basicInfo.minPrice, //选择产品规格的价格
        score: goodsDetail.basicInfo.minScore,
        left: "",
        active: true,
        number: plus,
        logisticsType: goodsDetail.basicInfo.logisticsId,
        logistics: goodsDetail.logistics,
        weight: goodsDetail.basicInfo.weight
      }
    }
  }
})