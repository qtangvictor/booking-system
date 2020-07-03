# _*_ coding:utf-8 _*_
# file name: sql_handle.py
#import mysql.connector
import MySQLdb
import datetime
class sqlconn(object):
	def __init__(self,hs,us,pw,pt,dbs,chs):
		self.conn=MySQLdb.connect(host=hs,user=us,passwd=pw,port=pt,db=dbs,charset=chs)
		self.cursor=self.conn.cursor()
	
	def select_coachschedule(self,coach_name):
		# this function return the scheduled time for a specific coach in the future 5 days
		datestart=datetime.date.today()+datetime.timedelta(days=1)
		dateend=datetime.date.today()+datetime.timedelta(days=6)
		datestart=datetime.datetime(datestart.year,datestart.month,datestart.day,10)
		dateend=datetime.datetime(dateend.year,dateend.month,dateend.day,22)

		sqlcommand="""SELECT s.datetime FROM schedule s
		INNER JOIN coach c
		ON s.coa_id=c.id
		WHERE c.name=%s AND s.datetime>=%s AND s.datetime<=%s """
		self.cursor.execute(sqlcommand,(coach_name,datestart,dateend))
		result=self.cursor.fetchall()
		date_occu=[]
		for (row,) in result:
			date_occu.append(row)
		return date_occu
	
	def add_schedule(self,cus_id,dttm,coach_name,ms):
		# this fuction insert the appointed time and the remaining membership into database 
		sqlcommand="""SELECT id FROM coach WHERE name=%s"""
		self.cursor.execute(sqlcommand,(coach_name,))
		result=self.cursor.fetchone()
		coach_id=int(result[0])

		sqlcommand="""INSERT IGNORE INTO schedule(wechat_id,datetime,coa_id) VALUES (%s,%s,%s)""" 
		self.cursor.execute(sqlcommand,(cus_id,dttm,coach_id))

		sqlcommand="""UPDATE customer SET membership=%s WHERE wechat_id=%s""" 
		self.cursor.execute(sqlcommand,(ms,cus_id))
		self.conn.commit()
	
	def select_customerschedule(self,cus_id):
		#this function return the booked time for a specific customer
		current_datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		sqlcommand="""SELECT datetime FROM schedule WHERE wechat_id=%s AND datetime>%s"""
		self.cursor.execute(sqlcommand,(cus_id,current_datetime))
		result=self.cursor.fetchall()
		date_cus=[]
		for (row,) in result:
			date_cus.append(row)
		return date_cus
	
	def delete_schedule(self,cus_id,dttm,ms):
		# this function  delete the appointed time from database and increase the membership by 1
		sqlcommand="""DELETE FROM schedule WHERE wechat_id=%s AND datetime=%s"""
		self.cursor.execute(sqlcommand,(cus_id,dttm))

		sqlcommand="""UPDATE customer SET membership=%s WHERE wechat_id=%s"""
		self.cursor.execute(sqlcommand,(ms,cus_id))
		self.conn.commit()

	def add_customer(self,cus_id,nickn):
		sqlcommand="""INSERT IGNORE INTO customer(wechat_id,nickname) VALUES (%s,%s)"""
		self.cursor.execute(sqlcommand,(cus_id,nickn))
		self.conn.commit()

	def select_membership(self,cus_id):
		sqlcommand="""SELECT membership FROM customer WHERE wechat_id=%s"""
		self.cursor.execute(sqlcommand,(cus_id,))
		result=self.cursor.fetchall() #result is a tuple
		result_list=[]
		for (row,) in result:
			result_list.append(row)
		return int(result_list[0])

	def select_accesstoken(self):
		current_datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		sqlcommand="""SELECT access_token FROM accesstoken WHERE expire>%s"""
		self.cursor.execute(sqlcommand,(current_datetime,))
		result=self.cursor.fetchall() #result is a tuple
		if result:
			result_list=[]
			for (row,) in result:
				result_list.append(row)
			return result_list[0]
		else:
			return []
		

	def add_accesstoken(self,token,expire_in):
		sqlcommand="""INSERT INTO accesstoken(access_token,expire) VALUES (%s,%s)"""
		expire_time=datetime.datetime.now()+datetime.timedelta(seconds=expire_in)
		expire_time=expire_time.strftime('%Y-%m-%d %H:%M:%S')
		self.cursor.execute(sqlcommand,(token,expire_time))
		self.conn.commit()

	def overdue_schedule(self):
		# this function is to delete the overdue schedule
		pass










