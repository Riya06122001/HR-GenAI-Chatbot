# hr_genai_app/urls.py
from django.urls import path
from . import views
 
 
urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat_view, name='chat'),
]
 