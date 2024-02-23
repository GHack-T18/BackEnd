from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import User1,User2,User3
from django.contrib.auth.hashers import make_password
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout , login as dj_login

#________________Login________________________________________#

@api_view(['GET'])
def redirect_loggedin_user(request):
    """
    Redirects logged-in user to appropriate page based on their role.
    Retrieves the user's role (administrateur, Moderateur, utilisateur) and returns the appropriate response.
    """
   
    user = request.user
    User1_exists = User1.objects.filter(user_id=user.id).exists()
    User2_exists = User2.objects.filter(user_id=user.id).exists()
    User3_exists = User3.objects.filter(user_id=user.id).exists()

    if user.is_staff:
        return Response({'user': 'administrateur'})

    if User1_exists:
        user1 = User1.objects.get(user=user)
        return Response({'user': 'User1'})

    if User2_exists:
        user2= User2.objects.get(user=user)
        return Response({'user': 'User2'})
    
    if User3_exists:
        user3= User3.objects.get(user=user)
        return Response({'user': 'User3'})
    
    return Response({'user': 'Non trouvé'})
