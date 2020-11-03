from django.urls import path
from . import views
urlpatterns = [
path('', views.index),
path('signin', views.signin),
path('register', views.register_form),
path('login', views.login),
path('dashboard', views.dashboard),
path('registration', views.registration),
path('myaccount/<int:id>', views.edit_account),
path('back', views.back),
path('logout', views.logout)
]