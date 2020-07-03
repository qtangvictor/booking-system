# -*- coding: utf-8 -*-
# filename: basic.py
# this module is to get the accesstoken automatically
import urllib
import time
import json
class Basic:    
	def __init__(self):        
		self.__accessToken = ''        
		self.__leftTime = 0    
	def __real_get_access_token(self):       
		appId = "wx78f5ac13c57b4f54"        
		appSecret = "3c07d9525bc5f707039e2d4d215da969"        
		postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appId, appSecret))        
		urlResp = urllib.urlopen(postUrl)        
		urlResp = json.loads(urlResp.read())                
		self.__accessToken = urlResp['access_token']        
		self.__leftTime = urlResp['expires_in']    
	def get_access_token(self):        
		if self.__leftTime < 10:            
		 	self.__real_get_access_token()        
		return self.__accessToken,self.__leftTime    
	def run(self):        
		while(True):            
			if self.__leftTime > 10:                
				time.sleep(2)
				self.__leftTime -= 2
			else:                
				self.__real_get_access_token()