from django import forms
from django.forms import ModelForm
from chatbot.models import UserSession

class UserSessionForm(ModelForm):
	class Meta:
		model = UserSession
		fields = ['user_name', 'gender']


class UserSessionTwoForm(ModelForm):
	class Meta:
		model = UserSession
		fields = ['user_text']

class UserSessionVisit(ModelForm):
	class Meta:
		model = UserSession
		fields = ['visits']

class UserSessionUserS(ModelForm):
	class Meta:
		model = UserSession
		fields = ['user_session']

