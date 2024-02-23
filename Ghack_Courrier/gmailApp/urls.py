from django.urls import path
from . import views

urlpatterns = [
    path('gmailconnect/',views.get_emails,name='gmailconnect'),
]