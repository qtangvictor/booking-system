# -*- coding: utf-8 -*-
# filename: book.py
import web
import datetime
import sql_handle
import sae.const
import urllib
import json
class Book:
	def GET(self):   	
		try:
			i=web.input()
			coachid=int(i.coachid) # 获取从menu url中传入的教练id (e.g. /book?coachid=1)
			coach_list=['张三','李四','王五'] 
			coach=coach_list[coachid-1] # get the coach name from url
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


			#date=[datetime.datetime(2019, 4, 15, 10, 0),datetime.datetime(2019, 4, 15, 11, 0),datetime.datetime(2019, 4, 15, 12, 0),datetime.datetime(2019, 4, 15, 16, 0),datetime.datetime(2019, 4, 16, 10, 0),datetime.datetime(2019, 4, 16, 11, 0),datetime.datetime(2019, 4, 16, 19, 0),datetime.datetime(2019, 4, 16, 20, 0),datetime.datetime(2019, 4, 17, 10, 0),datetime.datetime(2019, 4, 17, 11, 0),datetime.datetime(2019, 4, 17, 12, 0),datetime.datetime(2019, 4, 17, 13, 0)]
			#occupy_date=[datetime.datetime(2019, 4, 15, 11, 0),datetime.datetime(2019, 4, 16, 10, 0)]
			def create_date(): 
				# this function is to get the working hours for the following 5 days
				# the working hour is from 10-22
				time_list=[]
				datestart=datetime.date.today()+datetime.timedelta(days=1)
				dateend=datetime.date.today()+datetime.timedelta(days=6)
				datestart=datetime.datetime(datestart.year,datestart.month,datestart.day,10)
				dateend=datetime.datetime(dateend.year,dateend.month,dateend.day,22)
				while datestart<=dateend:
					time_list.append(datestart)
					if datestart.hour<22:
						datestart+=datetime.timedelta(hours=+1)
					else:
						datestart+=datetime.timedelta(hours=+12)
				return time_list
			date=create_date() #all time points			
			
			connect=sql_handle.sqlconn(sae.const.MYSQL_HOST,sae.const.MYSQL_USER,sae.const.MYSQL_PASS,int(sae.const.MYSQL_PORT),sae.const.MYSQL_DB,'utf8')
			connect.add_customer(openid,nickname) #add customer info into database. if existing, ingore.
			occupy_date=connect.select_coachschedule(coach) # get unavailable time points
			number=connect.select_membership(openid) # get the remaining membership

			unique_date=[] # the unique date of the schedule
			for i in date:
				if i.strftime('%y-%m-%d') not in unique_date:
					unique_date.append(i.strftime('%y-%m-%d'))
	
			time=[] #all the time points of the shcedule. it's a two-dimention list. the length of the list is the number of the day.
			time_temp=[]
			p=0

			for i in date:
				if i.strftime('%y-%m-%d')==unique_date[p]:
					time_temp.append(i.strftime('%H:%M'))
				else:
					time.append(time_temp)
					p+=1
					time_temp=[]
					time_temp.append(i.strftime('%H:%M'))
			time.append(time_temp)

			time_occupy={} # the time points that are unavailable. it's a dictionary. the key is the date and the value is the time.
			time_temp=[]
			p=0
			for i in range(len(unique_date)):
				time_occupy[unique_date[i]]=[]
			for i in occupy_date:
				time_occupy[i.strftime('%y-%m-%d')].append(i.strftime('%H:%M'))
	        
			render = web.template.render('templates/')
			return render.book(coach,unique_date,time,time_occupy,number,openid)
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
		coach= inputall.coach
		date= inputall.date
		time= inputall.time
		membership=inputall.membership
		openid=inputall.openid
		membership=int(membership)
		membership-=1

		#print("coach: %s date: %s time: %s membership: %s openid: %s" % (coach,date,time,membership,openid))
		#return "Great success! coach: %s date: %s time: %s membership: %s" % (coach,date,time,membership)
		#web.seeother('/')

		#把数据写进数据库
		try:
			connect=sql_handle.sqlconn(sae.const.MYSQL_HOST,sae.const.MYSQL_USER,sae.const.MYSQL_PASS,int(sae.const.MYSQL_PORT),sae.const.MYSQL_DB,'utf8')
			connect.add_schedule(openid,'20'+date+' '+time,coach,membership)  
			return membership 
		except Exception, Argment:
			if 'connect' in dir():
				connect.conn.rollback
			return Argment
		finally:
			if 'connect' in dir():
				connect.cursor.close()
				connect.conn.close()





		