from django.urls import path
from django.urls import reverse
from . import views
import twitter.views

app_name = 'chatbot'

urlpatterns = [
    path("chatbot/<uuid>/", views.chatbot, name='chatbot_chatbot'),
    path("post/<uuid>/", views.chatbot_process, name='post'),
    path("", views.landing, name='home'),

]
