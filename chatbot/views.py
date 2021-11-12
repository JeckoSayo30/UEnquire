from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

from twitter.models import *
from django.contrib import messages
from .forms import *
from googletrans import Translator
translator = Translator()
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
# =============================================================
# FOR TRAINING-CHATBOT IMPORT
import os
import random
import json
import pickle
import numpy as np
import nltk
nltk.download('wordnet')
nltk.download('punkt')
from nltk.stem import WordNetLemmatizer
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Activation, Dropout
# from tensorflow.keras.optimizers import SGD
from tensorflow.keras.models import load_model
# ============================================================
#NEW IMPORT
import ftfy
from django.views.decorators.cache import cache_control
# ============================================================

#FOR TWITTER-API IMPORT
# import tweepy
# import pandas as pd
# Create your views here.
# ===============================================================
def chatbot_process(request, uuid):
	#INITIALIZATION CHATBOT 
	lemmatizer = WordNetLemmatizer()
	intents = json.loads(open('twitter/intents.json').read())

	words = pickle.load(open('words.pkl', 'rb'))
	classes = pickle.load(open('classes.pkl', 'rb'))

	model = load_model('chatbotmodel.h5')

	# FUNCTION DEFINITION
	def clean_up_sentence(sentence):
	    sentence_words = nltk.word_tokenize(sentence)
	    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
	    return sentence_words

	def bag_of_words(sentence):
	    sentence_words = clean_up_sentence(sentence)
	    bag = [0] * len(words)
	    for w in sentence_words:
	        for i, word in enumerate(words):
	            if word == w:
	                bag[i] = 1
	    return np.array(bag)

	def predict_class(sentence):
	    bow = bag_of_words(sentence)
	    res = model.predict(np.array([bow]))[0]
	    ERROR_THRESHOLD = 0.25
	    results = [[i,r]for i, r in enumerate(res) if r > ERROR_THRESHOLD]

	    results.sort(key = lambda x: x[1], reverse = True)
	    return_list = []
	    for r in results:
	        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
	    return return_list

	def get_response(intents_list, intents_json):
	    tag = intents_list[0]['intent']
	    list_of_intents = intents_json['intents']
	    for i in list_of_intents:
	        if i ['tag'] == tag:
	            result = random.choice(i['responses'])
	            break
	    
	    return result

	# TAKING OF INPUT MESSAGES	
	message = request.GET.getlist('input_text')
	messageTwo = ' '.join([str(elem) for elem in message]) 
	messageTwo = messageTwo.lower()

	translate_words = translator.translate(messageTwo, dest="en")
	result_translate = translate_words.text
	ints = predict_class(str(result_translate))
	response = get_response(ints, intents)
	response = ftfy.fix_text(str(response))

	context = {
	'response':response
	}

	obj = UserSession.objects.get(uuid=uuid)
	# user_v = request.GET.get('user_Visits')
	# print(user_v,"<<++++ VISIT")
	

	# SAVING USER INPUT INTO DATABASE	
	user_text = request.GET.getlist('user_text')
	user_textString = ' '.join([str(elem) for elem in user_text]) 
	translate_NewWords = translator.translate(user_textString, dest="en")
	result_Newtranslate = translate_NewWords.text
	
	
	form = UserSessionTwoForm({'user_text':result_Newtranslate }, instance=obj)
	if form.is_valid():
		form.save()
	return HttpResponse(response)
	

@cache_control(no_cache=True, must_revalidate=True)
def chatbot(request, uuid):
	if request.method=='POST' and 'endSessions' in request.POST:
		user_sessions1 = UserSession.objects.filter(uuid = uuid)
		for user_ses in user_sessions1:
			session = request.session._get_or_create_session_key()
			user_key = UserSession.objects.filter(uuid=uuid).update(user_session=None)
			print("DELETED SESSION KEY")
			return redirect('chatbot:home')

	if request.session.session_key == None:
		return redirect('/')

	user = UserSession.objects.get(uuid=uuid)
	session = request.session._get_or_create_session_key()
	user.user_session = session
	user.save()
	obj = user.uuid
	osy = user.user_name

	user_visits = request.session['visits'] = int(request.session.get('visits',0)) + 1
	form2 = UserSessionVisit({'visits': user_visits}, instance=user)
	if form2.is_valid():
		form2.save()

	links_model = linksModel.objects.all()
	context={
	'obj':obj, 'user_visits':user_visits, 'links':links_model
	}
	
	return render(request, "chatbot/chatbot.html",context)
	
	
def landing(request):
	if request.method == 'POST':
		user = UserSessionForm(request.POST)
		if user.is_valid():
			user2 = request.POST.get('user_name')
			gender = request.POST.get('gender')
			request.session['user2'] = user2.capitalize()
			request.session['gender'] = gender
			obj = user.save() 
			return redirect('chatbot:chatbot_chatbot', uuid=obj.uuid)
		else:
			messages.info(request, 'Please input')

	try:
		sessionTwo = request.session._get_or_create_session_key()
		user_key = UserSession.objects.get(user_session=sessionTwo)
		if user_key.user_session != None:
			session = request.session._get_or_create_session_key()
			user_key = UserSession.objects.get(user_session=session)
			print(user_key,"<<--")
			return redirect('chatbot:chatbot_chatbot',uuid=user_key.uuid)
	except:
		session = None
	return render(request,"chatbot/landing_page.html")

