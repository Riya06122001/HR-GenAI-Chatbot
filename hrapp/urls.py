# hr_genai_app/urls.py
from django.urls import path
from . import views
from .views import chat_view
 
 
urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', chat_view, name='chat'),
]
 