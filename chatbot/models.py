from django.db import models
import os, random
import uuid



LOCATION = (
		''
	)

# Create your models here.

class UserSession(models.Model):
	user_name = models.CharField(max_length=100, verbose_name='User Name')
	gender = models.CharField(max_length=50, verbose_name='Gender')
	user_text = models.TextField(verbose_name='User Input', null=True)
	user_session = models.CharField(max_length=150,verbose_name='User Session', null=True)
	uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	visits = models.IntegerField(verbose_name="Number of visit", null=True)
	class Meta:
		db_table = "user_session"

	def __str__(self):
		return self.user_name

	def get_abolute_url(self):
		return "/chatbot/%i/" % self.id
	def detail(self):
		return f"Username: {self.user_name}, gender: {self.gender}, Session: {self.user_session}"




#LOST N FOUND TABLE
class LostNFound(models.Model):
	reg_id = models.AutoField(primary_key=True, verbose_name='ID')
	name = models.CharField(max_length=100, verbose_name='Name')
	stud_num = models.CharField(max_length=11, verbose_name = "Student Number")
	email = models.EmailField(unique=True, max_length=50, verbose_name='Email', blank=True)
	contact = models.CharField(max_length=11, verbose_name='Contact Number')

	found  = models.BooleanField(default=False, verbose_name="Found?")
	lost = models.BooleanField(default=False, verbose_name="Lost?")

	item = models.CharField(max_length=100,verbose_name='Item')   
	item_desc = models.TextField(max_length=500,verbose_name='Item Description')  

	pick_up_loc = models.CharField(max_length=100, verbose_name='Pick-up Location', default="SAO office")

	def __str__(self):
		return self.name
