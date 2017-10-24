# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from models import User
from django.contrib import messages

# Route ('/')
def index(request):
	# User.objects.all().delete()
	return render(request,'login_app/index.html')

#*********************************************************************************

#Route ('/register')
def register(request):
	result=User.objects.registerVal(request.POST) #refer to validation function in models.
	if result['status']==False:
		User.objects.createUser(request.POST) #refer to create function in models adding user to database.
		messages.success(request,'Your account has been created. Please log in') 
	else: #if validation result in errors, key messages in result list will display.
		for error in result['errors']:
			messages.error(request,error)
	return redirect('/')

#************************************************************************************	

def login(request):
	results=User.objects.loginVal(request.POST)
	if results['status']==True:
		for error in results['errors']:
			messages.success(request,error)
		return redirect('/')
	else:
		request.session['first_name']=results['user'].first_name
		request.session['last_name']=results['user'].last_name
		request.session['id']=results['user'].id
		request.session['email']=results['user'].email
		# request.session['birthdate']=results['user'].birthdate
		return redirect('/main')

#**********************************************************************************

def logout(request):
	request.session.clear()
	return redirect('/')