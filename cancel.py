# -*- coding: utf-8 -*-
# filename: cancel.py
import web
import datetime
import sql_handle
import sae.const
import urllib
import json
class Cancel:
	def GET(self):   	
		try:
			i=web.input()
			code=i.code #获取code
			appID = "wx78f5ac13c57b4f54"
			appsecret="3c07d9525bc5f707039e2d4d215da969"
			def getUserInfo(appID,appsecret,code):
				#使用code换取access_token和openid
				#使用access_token和openid获取用户昵称
				access_token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid="+appID+"&secret="+appsecret+"&code="+code+"&grant_type=authorization_code"
				urlResp = urllib.urlopen(access_token_url)
				urlResp = json.loads(urlResp.read())
				access_token=urlResp['access_token']
				openid=urlResp['openid']
				userinfo_url = "https://api.weixin.qq.com/sns/userinfo?access_token="+access_token+"&openid="+openid+"&lang=zh_CN"
				urlResp = urllib.urlopen(userinfo_url)
				urlResp = json.loads(urlResp.read())
				nickname=urlResp['nickname']
				return openid,nickname
			openid,nickname=getUserInfo(appID,appsecret,code)

			connect=sql_handle.sqlconn(sae.const.MYSQL_HOST,sae.const.MYSQL_USER,sae.const.MYSQL_PASS,int(sae.const.MYSQL_PORT),sae.const.MYSQL_DB,'utf8')
			datetime=connect.select_customerschedule(openid) # get customer's schedule
			number=connect.select_membership(openid) # get the remaining membership

			date=[]
			for i in datetime:
				date.append(i.strftime('%y-%m-%d %H:%M'))

			render = web.template.render('templates/')
			return render.cancel(date,number,openid)
		except Exception, Argment:
			if 'connect' in dir():
				connect.conn.rollback
			return Argment
		finally:
			if 'connect' in dir():
				connect.cursor.close()
				connect.conn.close()

	def POST(self):
		inputall =web.input() #获取从表单中返回的数据
		datetime= inputall.datetime #要取消的时间
		membership=inputall.membership 
		openid=inputall.openid
		membership=int(membership)
		membership+=1 #次数加一

		#print("datetime: %s membership: %s openid: %s" % (datetime,membership,openid))
		#return "Great success! coach: %s date: %s time: %s membership: %s" % (coach,date,time,membership)
		#web.seeother('/')

		#删除数据库中的预约时间 修改次数
		try:
			connect=sql_handle.sqlconn(sae.const.MYSQL_HOST,sae.const.MYSQL_USER,sae.const.MYSQL_PASS,int(sae.const.MYSQL_PORT),sae.const.MYSQL_DB,'utf8')
			connect.delete_schedule(openid,'20'+datetime,membership)  
			return membership 
		except Exception, Argment:
			if 'connect' in dir():
				connect.conn.rollback
			return Argment
		finally:
			if 'connect' in dir():
				connect.cursor.close()
				connect.conn.close()





		