from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('', views.preolad, name='preload'),
    path('home', views.say_hello, name='home'),
    path('floor/<str:i>',views.views_floor)
]