# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.contrib import messages
from ..login_app.models import User
from models import Pet

# Create your views here.
def main(request):
	context={
		'mypets':User.objects.get(id=request.session['id']),
		'other_user': User.objects.exclude(id=request.session['id'])
	}
	return render(request,'main_app/index.html',context)
def addpet(request):

	return render(request, 'main_app/addpet.html')	

def createpet(request):
	results=Pet.objects.validation(request.POST)
	if len(results['errors'])>0:
		for error in results['errors']:
			messages.error(request,error)
		return redirect('/addpet')
	Pet.objects.create(name=request.POST['name'], kind=request.POST['kind'],owner=User.objects.get(id=request.session['id']))
		#creating a comment belong to either the poster or the other user in database. 
	return redirect('/main')	
def delete(request,id):
	Pet.objects.get(id=id).delete()
	return redirect('/main')	

def show(request,id):
	context={
		'user': User.objects.get(id=id)
	}
	return render(request, 'main_app/show.html',context)