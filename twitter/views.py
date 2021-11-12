from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import pandas as pd
from django.contrib.auth.models import User
import os
import random
import json

from tensorflow.keras.models import load_model
# ============================================================
import subprocess
from .models import *
from .forms import *
import re
# ============================================================
from twitter.forms import SourceForm, RegistrationForm, AccountAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password , check_password
from django.contrib import messages
from twitter.decorators import unauthenticated_user, allowed_users
# ============================================================
from django.views import View
from django.template import loader
# ============================================================
# from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView

from django.core.files.storage import FileSystemStorage

# ========================================================================================
class CrudView(ListView):
    model = Source
    template_name = 'twitter/Crud.html'
    context_object_name = 'source'

class CreateCrudUser(View):
    def  get(self, request):
    	print("<<<<<=================EDIIIITTT========================")
    	name_source = request.GET.get('source_acct', None)
    	print(name_source)
    	obj = Source.objects.create(source_acct = name_source)

    	source = {'twitter_id':obj.twitter_id,'source_acct':obj.source_acct}
    	data = {'source': source}

    	return JsonResponse(data)


class linksViesUTwo(View):
    def  get(self, request):
    	print("<<<<<=================EDIIIITTT========================")
    	link_name = request.GET.get('link_name', None)
    	links = request.GET.get('links', None)
    	obj = linksModel.objects.create(link_name = link_name, links = links)
    	source = {'link_id':obj.link_id,'link_name':link_name, 'links':obj.links}
    	data = {'source': source}
    	return JsonResponse(data)

# ========================================================================================
# UPLOAD DATASET FOR NAIVE BAYES 

from twitter.backend import uploads 
def upload(request):
	files = analyticsUpload.objects.all()
	context = {
		'files': files,
		'classifier_settings': ClassifierSettings.objects.all().last(),
		'model_desc': ClassifierModels.objects.all().last()
	}

	if request.method == 'POST' and 'upload' in request.POST:
		request = uploads.naive_bayes_upload(request, analyticsUpload)

	# Admin inputs
	if request.method == 'POST' and 'new_settings' in request.POST:
		size = request.POST.get('test_size')
		state = request.POST.get('random_state')
		ave = request.POST.get('average')
		entry = ClassifierSettings(test_size=size, rand_state=state, average=ave)
		entry.save()

	return render(request, "twitter/upload_file/analytics_upload.html", context)
# ========================================================================================
# TRAINING OF CLASSIFIER MODEL/ NAIVE BAYES
from twitter.backend import training_classifier as classifier
def train_classifier(request):		
	if request.method == 'POST' and 'train_model' in request.POST:
		file = request.POST.get('train_model')
		file_obj = analyticsUpload.objects.get(name=file)


		# Classifier training(NAIVE BAYES)
		if ClassifierSettings.objects.all().count() != 0:
			settings = ClassifierSettings.objects.all().last()
			model, scores, vectorizer = classifier.naive_bayes(file_obj.file, settings.test_size, settings.rand_state, settings.average)
			entry = ClassifierModels(
				correct=scores['correct'],
				incorrect=scores['incorrect'],
				accuracy=scores['accuracy'],
				recall=scores['recall'],
				precision=scores['precision'],
				f1_score=scores['f1_score']
				)
			entry.save()
		else:
			print("EMPTY CLASSIFIER SETTINGS")
		# sample = ["The University of East has announced suspension.","Corrupted politicians are not hero",
		# "Be sure to vote on the upcomming election", "Signal number 3 sa Bicol", "sd;oosfskfj", 
		# "The Student Council has an important announcement to make this week", 
		# "The UE Journalism has an important integrity to uphold",

		# "university of the east is close for holiday.",
		# "Ester Garcia nag announce ng walang pasok sa buong linggo",
		# "manny paquiao for president!",
		# "urgent just in advisory breaking news"
		# ]
		# matrix = vectorizer.transform(sample)
		# print(model.predict(matrix))
		
	return HttpResponse("CLASSIFIER TRAINING COMPLETE")
# ========================================================================================
# DOWNLOAD TWEETS EXCEL
from twitter.backend import download_file as dl
def download_excel(request):
	request = dl.excel_dl(Tweets)
	return request
# ========================================================================================
# TWITTER MAIN TABLE 
from twitter.backend import tw_backend as tw
@login_required(login_url='twitter:login')
def twitter_data(request):
	api = tw.open_acct()
	num_post = 1
	# Admin Inputs
	if request.method == 'POST' and 'num_posts' in request.POST:
		num_post = int(request.POST.get('number'))

	if request.method == 'POST' and 'sour_sub' in request.POST:
		sources = SourceForm(request.POST)
		if sources.is_valid():
			sources.save()
		else:
			print("Invalid")
	if Source.objects.all().count() == 0:
		accounts = []
	else:
		accounts = Source.objects.all()
		accounts = tw.output(accounts, api, num_post)		
	# CONTEXT
	tweets = Tweets.objects.all()
	context = {'tweets': tweets, 'source_list': accounts}
	return render(request, "twitter/analytics.html", context)
# ========================================================================================
# INTENTS MAIN TABLE
from twitter.backend import intents_backend as intent 
@login_required(login_url='twitter:login')
def intents(request):
	form, data = intent.open_intents(Intents)

	if request.method == 'POST':
		form, new_obj, data, request = intent.request_POST(request, data)	
		with open("twitter/intents.json", 'w') as data_file:
			json.dump(data, data_file, indent=4)
		return JsonResponse({'new_form': new_obj})

	return render(request, "twitter/chatbot_intents.html", {'intents': form})

# class linksViesUTwo(View):
#     def  get(self, request):
#     	print("<<<<<=================EDIIIITTT========================")
#     	link_name = request.GET.get('link_name', None)
#     	links = request.GET.get('links', None)
#     	obj = linksModel.objects.create(link_name = link_name, links = links)
#     	source = {'link_id':obj.link_id,'link_name':link_name, 'links':obj.links}
#     	data = {'source': source}
#     	return JsonResponse(data)
# ========================================================================================
class intentsDeleteView(View):
	
	def get(self,request, pk, *args, **kwargs):
		
		if request.is_ajax():
			print("<<<<<=================DELETE========================")
			tag = Intents.objects.get(pk=pk)
			tag_name = str(tag.tag)
			tag.delete()
			with open("twitter/intents.json", "r") as file:
				data = json.load(file)	

			for item in data["intents"]:
				if item["tag"] == tag_name:
					data["intents"].remove(item)

			with open("twitter/intents.json", 'w') as data_file:
				json.dump(data, data_file, indent=4)

			return JsonResponse({"message":"success"})
		return JsonResponse({"message": "Wrong request"})

class sourcesDeleteView(View):
	def get(self,request, pk, *args, **kwargs):
		if request.is_ajax():
			print("<<<<<=================DELETE========================")
			source = Source.objects.get(pk=pk)
			source.delete()
			return JsonResponse({"message":"success"})
		return JsonResponse({"message": "Wrong request"})

class linksDeleteView(View):
	def get(self,request, pk, *args, **kwargs):
		if request.is_ajax():
			print("<<<<<=================DELETE========================")
			source = linksModel.objects.get(pk=pk)
			source.delete()
			return JsonResponse({"message":"success"})
		return JsonResponse({"message": "Wrong request"})
# ========================================================================================
# TRAINING OF CHATBOT MODEL 
from twitter.backend import training_chatbot as train_bot
def train_data(request):
	train_bot.chatbot_training()
	return render(request, "twitter/train.html", {})

# ========================================================================================
#  WEBSCRAPING THE UE WEBSITE
from twitter.backend import ue_data 
def uedata(request):
	request = ue_data.site(request)
	return HttpResponse("UE DATA UPLOADED SUCCESSFULL")

def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect

# =======================================================================
@unauthenticated_user
def accounts_login(request, *args, **kwargs):
	context = {}
	if request.method=='POST' and 'signUp' in request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			# Account created successfully
			form.save()

			# After registration they are to be logged in
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email,password=raw_password)
			login(request,account,backend='django.contrib.auth.backends.ModelBackend')
			
			# san to nakuha??
			destination = kwargs.get("next")
			if destination:
				return redirect(destination)

			messages.info(request, 'Account created successfully')
			return redirect("twitter:login")
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form

	
	destination = get_redirect_if_exists(request)
    #===============================================================================
	# SIGNIN 
	if request.method=='POST' and 'signIn' in request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			
			messages.info(request, 'You logged in.')
			if user:
				login(request, user)
				if destination:
					return redirect(destination)
				return redirect("twitter:chatbot-twitter-data")
			else: 
				print("--------------------------------------------")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	return render(request, "twitter/loginANDregister.html",context)

def logout_view(request):
	logout(request)
	return redirect("twitter:login")



def side(request):
	return render(request, "twitter/sidebar_and_head/sidebar.html")


@login_required(login_url='twitter:login')
def links(request):
	formTwo = linksModel.objects.all()
	context={'links':formTwo}
	return render(request, "twitter/links.html", context)
