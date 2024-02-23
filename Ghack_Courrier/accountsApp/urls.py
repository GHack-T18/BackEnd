from django.urls import path
from . import views

urlpatterns = [
    path('redirect/',views.redirect_loggedin_user,name='login'),
    path('addUser1/',views.Add_User1,name='addUser1'),
    path('addUser2/',views.Add_User2,name='addUser2'),
    path('addUser3/',views.Add_User3,name='addUser3'),
    path('userinfo/',views.current_user,name='user_info'),

]