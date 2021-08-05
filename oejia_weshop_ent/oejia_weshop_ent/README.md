### OE商城(小程序)基本使用配置说明

1. 安装依赖的python包
```
pycrypto
xmltodict==0.11.0
itsdangerous==0.24
kdniao==0.1.2
wechatpy
```
2. 将交付的模块（oejia_weshop、oejia_weshop_ent、task_queue 等解压后的目录）放到您的 addons 目录（odoo的插件目录）下
3. 重启odoo服务，更新本地应用列表，安装oejia_weshop_ent模块，可以看到Odoo产生了顶部“电商”主菜单
4. 进入【设置】-【对接设置】页填写您的微信小程序相关对接信息
5. 小程序客户端: wechat-app-mall, 用微信官方IDE打开后修改接口api调用地址和appid即可，具体如下：
- 将 wxapi/main.js 中第3行的 API_BASE_URL 改为：https://您的odoo地址/wxa（例如：https://sale.calluu.cn/wxa）
- 将 config.js 中第5行的 appid 改为您的小程序的 appid