from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User

from .models import *
# Register your models here.

class User(admin.ModelAdmin):
	list_display = ['user_name','gender']
	search_fields = ['user_name','gender']

	readonly_fields = ['user_session', 'uuid', 'visits']


admin.site.register(UserSession, User)