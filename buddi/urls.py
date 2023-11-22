from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('signup',views.signup, name='signup'),
    path('login',views.login, name='login'),
    path('newsfeed', views.newsfeed, name='newsfeed'),
    path('logout', views.logout, name='logout'),
    path('upload',views.upload,name='upload'),
]

