# -*- coding: utf-8 -*-
# filename: menu.py
import urllib
from basic import Basic

class Menu(object):
    def __init__(self):
        pass
    def create(self, postData, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        if isinstance(postData, unicode):
            postData = postData.encode('utf-8')
        urlResp = urllib.urlopen(url=postUrl, data=postData)
        print urlResp.read()

    def query(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        print urlResp.read()

    def delete(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        print urlResp.read()

    #获取自定义菜单配置接口
    def get_current_selfmenu_info(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        print urlResp.read()

# the following can be deleted
if __name__ == '__main__':
    myMenu = Menu()
    postJson = """
{
    "button": [
        {
            "name": "私教预约", 
            "sub_button": [
                {
                    "type": "view", 
                    "name": "张三", 
                    "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx78f5ac13c57b4f54&redirect_uri=http://tangqian.applinzi.com/book?coachid=1&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect"
                }, 
                {
                    "type": "view", 
                    "name": "李四", 
                    "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx78f5ac13c57b4f54&redirect_uri=http://tangqian.applinzi.com/book?coachid=2&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect"
                }, 
                {
                    "type": "view", 
                    "name": "王五", 
                    "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx78f5ac13c57b4f54&redirect_uri=http://tangqian.applinzi.com/book?coachid=3&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect"
                }
            ]
        }, 
        {
            "type": "view", 
            "name": "取消预约", 
            "url": "http://tangqian.applinzi.com/cancel"
        }
    ]
}
    """
    accessToken = Basic().get_access_token()
    #myMenu.delete(accessToken)
    myMenu.create(postJson, accessToken)