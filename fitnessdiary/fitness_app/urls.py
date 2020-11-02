from django.urls import path
from . import views
urlpatterns = [
path('', views.index),
path('signin', views.signin),
path('register', views.register_form),
path('login', views.login),
path('dashboard/<int:id>', views.dashboard),
path('registration', views.registration),

]