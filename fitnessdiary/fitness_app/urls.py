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
path('logout', views.logout),
path('createroutine', views.createroutine),
path('delete_account', views.delete_account),
path('delete_routine/<int:id>', views.delete_routine),
path('update/<int:id>', views.update_account),
path('all_routines/<int:id>', views.all_routines),
path('create_routine', views.add_routine),
]