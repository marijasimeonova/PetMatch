from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('upload', views.upload, name='upload'),
    path('like_post', views.like_post, name='like_post'),
    path('search', views.search, name='search'),
    path('follow', views.follow, name='follow'),
    path('settings', views.settings, name='settings'),
    path('myposts', views.myposts, name='myposts'),
    path('delete_post', views.delete_post, name='delete_post'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
]
