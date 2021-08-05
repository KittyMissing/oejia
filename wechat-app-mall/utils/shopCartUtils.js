/**
 * 加入购物车
 */
function addToShopCart(goodsDetail, shopCarInfo) {
  // 加入购物车
  //var shopCarGood = bulidShopCarInfo(goodsDetail);
  //var shopCarInfo = getShopCarInfo();
  updateShopList(shopCarInfo.shopList, goodsDetail);

  // 计算购物车总件数， 总价格， 总积分
  shopCarInfo.shopNum = shopCarInfo.shopNum + goodsDetail.number;
  shopCarInfo.totalPrice = shopCarInfo.totalPrice + parseFloat(goodsDetail.price * goodsDetail.number);
  shopCarInfo.totalScore = shopCarInfo.totalScore + goodsDetail.score * goodsDetail.number;
  return shopCarInfo;
}

/**
 * 组建购物车信息
 */
function buildShopCarItem(goodsItem) {
  var shopCarItem = {};
  shopCarItem.goodsId = goodsItem.basicInfo.id;
  shopCarItem.pic = goodsItem.basicInfo.pic;
  shopCarItem.name = goodsItem.basicInfo.name;
  shopCarItem.price = goodsItem.basicInfo.minPrice;
  shopCarItem.score = goodsItem.basicInfo.minScore;

  // 物流信息
  shopCarItem.logisticsType = goodsItem.basicInfo.logisticsId;
  shopCarItem.logistics = goodsItem.logistics;
  shopCarItem.weight = goodsItem.basicInfo.weight;

  shopCarItem.active = true;
  shopCarItem.stores = goodsItem.basicInfo.stores;
  shopCarItem.propertyChildIds = "";
  shopCarItem.left = "";

  return shopCarItem
}

/**
 * 更新store, 如果购物车里面已经加入了改商品， 则只需修改产品number
 */
function updateShopList(shopList, shopCarMap) {
  var hasSameGoodsIndex = -1;
  for (var i = 0; i < shopList.length; i++) {
    var tmpShopCarMap = shopList[i];
    if (tmpShopCarMap.goodsId == shopCarMap.goodsId && (!tmpShopCarMap.propertyChildIds ||
        tmpShopCarMap.propertyChildIds == shopCarMap.propertyChildIds)) {
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
}

function getShopCarInfo() {
  var shopCarInfo = wx.getStorageSync('shopCarInfo');
  if (shopCarInfo && shopCarInfo != "" && Object.keys(shopCarInfo).length > 0) {
    return shopCarInfo;
  }

  shopCarInfo = {
    shopList: [],
    totalPrice: 0,
    shopNum: 0,
    totalScore: 0
  };
  return shopCarInfo;
}

module.exports = {
  addToShopCart: addToShopCart,
  getShopCarInfo: getShopCarInfo,
  buildShopCarItem: buildShopCarItem
}