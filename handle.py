# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import web
import reply
import receive
import sql_handle
import re
import sae.const
import xml.etree.ElementTree as ET
from basic import Basic
from menu import Menu
class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "tangqian" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument
    def POST(self):
        webData = web.data()
        #print "Handle Post webdata is ", webData
        xmlData = ET.fromstring(webData)
        msg_type = xmlData.find('MsgType').text
        #recMsg = receive.parse_xml(webData) # a instance of class TextMsg including including info from received msg
        #print(msg_type)
        if msg_type=='event':
            connect=sql_handle.sqlconn(sae.const.MYSQL_HOST,sae.const.MYSQL_USER,sae.const.MYSQL_PASS,int(sae.const.MYSQL_PORT),sae.const.MYSQL_DB,'utf8')
            accesstoken=connect.select_accesstoken()
            if accesstoken:
                pass
            else:
                accessToken,expire_in=Basic().get_access_token()
                print("accesstoken is:"+accessToken+" "+"expire in:"+str(expire_in))
                connect.add_accesstoken(accessToken,expire_in)
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
                            "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx78f5ac13c57b4f54&redirect_uri=http://tangqian.applinzi.com/cancel&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect"
                        }
                    ]
                }
                """
                myMenu.create(postJson, accessToken)
                return "success"


