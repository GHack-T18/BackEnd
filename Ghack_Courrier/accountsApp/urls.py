from django.urls import path
from . import views

urlpatterns = [
    path('redirect/',views.redirect_loggedin_user,name='login'),

]