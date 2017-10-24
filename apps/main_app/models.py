# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login_app.models import User
import re
Name_Regex = re.compile(r'^[A-Za-z ]+$')
# Create your models here.
class PetManager(models.Manager):
	def validation(self,postData):
		results={'errors':[]}
		for key in postData:
			if re.search(' ',postData[key]):
				results['errors'].append('No space please')	
		if not Name_Regex.match(postData['name']):
			results['errors'].append("Name can only be letters")		
		if len(postData['name'])<3:
			results['errors'].append('Name is too short')
		if not Name_Regex.match(postData['kind']):
			results['errors'].append("Type can only be letters")	
		if len(postData['kind'])<3:
			results['errors'].append('Type is too short')
		return results

class Pet(models.Model):
	name=models.CharField(max_length=255)
	kind=models.CharField(max_length=255)
	owner=models.ForeignKey(User,related_name='pets')
	objects=PetManager()