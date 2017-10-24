# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
# from datetime import date, datetime
# from time import strptime

Name_Regex = re.compile(r'^[A-Za-z ]+$')

class UserManager(models.Manager):
	
	def registerVal(self,postData): #validation on postData fields
		results={'errors':[], 'status':False} #creating object so to hold keys and value. Also a list to hold messages to warn user

		for key in postData:
			if re.search(' ',postData[key]):
				results['status']=True
				results['errors'].append('No space please')	
		if not Name_Regex.match(postData['first_name']):
			results['status']=True
			results['errors'].append("First name can only be letters")		
		if len(postData['first_name'])<2:
			results['status']=True
			results['errors'].append('First name is too short')
		if not Name_Regex.match(postData['last_name']):
			results['status']=True
			results['errors'].append("Last name can only be letters")	
		if len(postData['last_name'])<2:
			results['status']=True
			results['errors'].append('Last name is too short')
		
		if len(postData['password'])<4:
			results['status']=True
			results['errors'].append('Password is too short')
		if postData['password']!= postData['c_password']:
			results['status']=True
			results['errors'].append('Password do not match')

		# if str(date.today()) < str(postData['birthdate']):
		# 	results['status']=True
		# 	results['errors'].append("Please input a valid Date. Note: DOB cannot be in the future.")	
		
		if not re.match(r"[^@]+@[^@]+\.[^@]+", postData['email']): #email REGEX not match
			results['status']=True
			results['errors'].append('Invalid Email')
		
		user=self.filter(email=postData['email'])	#check if email already exist in database		
		if len(user)>0:	
			results['status']=True
			results['errors'].append('Email already exist')

		return results

	def createUser(self,postData): #adding user into database
		password=bcrypt.hashpw(postData['password'].encode(),bcrypt.gensalt()) #bcrypt password
		self.create(first_name=postData['first_name'],last_name=postData['last_name'],email=postData['email'],password=password)
		
	def loginVal(self,postData): #login validation.
		results={'errors':[],'status':False, 'user':None}
		email_matches=self.filter(email=postData['email']) 
		if len(email_matches)==0: #if email not match
			results['status']=True
			results['errors'].append('Please check your email and password and try again')
		else:
			results['user']=email_matches[0]
			if not bcrypt.checkpw(postData['password'].encode(), results['user'].password.encode()):	
				results['status']=True
				results['errors'].append('Please check your password')
		return results	
			

class User(models.Model):
	first_name=models.CharField(max_length=255)
	last_name=models.CharField(max_length=255)
	email=models.CharField(max_length=255)
	password=models.CharField(max_length=255)

	objects=UserManager()
