from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('signup',views.signup, name='signup'),
    path('login',views.login, name='login'),
    path('newsfeed', views.newsfeed, name='newsfeed'),
    path('logout', views.logout, name='logout'),
    path('upload',views.upload,name='upload'),
    path('like_post',views.like_post,name='like_post'),
    path('profile/<slug:pk>',views.profile,name='profile'),
    path('follow',views.follow,name='follow'),
    path('search',views.search,name='search'),
]

