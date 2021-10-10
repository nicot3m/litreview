from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('unsubscribe/<int:id_user_follow>', views.unsubscribe, name='unsubscribe'),
]
