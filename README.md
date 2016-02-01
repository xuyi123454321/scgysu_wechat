# USTC SCGY WeChat
# 中国科大少年班学院微信公众号后台

***********************************

## 计划实现的功能：
* “往期推送”，即分类历史消息。分为“小编推荐”、“特色活动”和“科技转窥”三项。
* “活动通道”：为少院同学提供最新的活动、讲座通知;建设活动报名平台，方便活动组织者与参与者;
  为活动的组织者提供方便的通知渠道。
* 在线抢课功能。

***********************************

## 已经完成的工作
* 与微信服务器交互凭证的定时获取。（ access_token.py )
* 服务器的配置、验证。（ /message_receive/view.py 中 url_check() )
* 基于历史消息分类的菜单构建、永久素材获取。( menu/ review/ )
* 抢课脚本的登录部分 （ https://github.com/xuyi123454321/lesson_robber.git )

***********************************

## 项目文件说                              
* /access_token.py :              获取与微信服务器的交互凭证
* /app_data.json :                存储微信公众号的appID与appsecret信息
* /uwsgi.ini :                    uwsgi配置文件
* /scgy_wechat/ :                 django主要的配置文件目录
* /static/ :                      静态文件
  * /static/review/ :             往期推送模块的静态文件
	* /static/review/style.css :    往期推送消息的样式表
	* /static/review/cover_pic/ :   从服务器下载到本地的消息封面图
* /message_receive/ :             监听、接受、分拣消息
  * /message_receive/views.py :   该模块的主程序，类似网页服务，接受get或post消息
* /menu/ :                        构建微信菜单同时建立往期推送所需的消息类型数据库
  * /menu/menu.py :               构造菜单
  * /menu/menu.json :             菜单内容
  * /menu/models.py :             菜单内容数据库
  * /menu/init_menu.py :          从menu.json构建数据库
* /review/ :                      往期推送模块
  * /review/models.py :           图文消息数据库
  * /review/grap.py :             定时从微信服务器获取图文消息、更新数据库、存储封面图
  * /review/views.py :            显示历史消息的网页
  * /review/templates/ :          网页模板目录
