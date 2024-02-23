from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import User1,User2,User3
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SingUpSerializer,UserSerializer

from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout , login as dj_login




'''--------------------------------------------------------------------------------------
    Login: pour les trois users:
        1:Administrateur: redirect vers 
        2:User1: 
        3:User2: 
        4:User3: 
--------------------------------------------------------------------------------------'''

@api_view(['GET'])
def redirect_loggedin_user(request):
    """
    Redirects logged-in user to appropriate page based on their role.
    Retrieves the user's role (administrateur, User1, User2, User3) and returns the appropriate response.
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



'''--------------------------------------------------------------------------------------
    Registration: pour les 4 users:
        1:Administrateur: avec la commande createsuperuser
        2:User1: la fonction Add_User1
        3:User1: la fonction Add_User2
        4:User1: la fonction Add_User3
--------------------------------------------------------------------------------------'''
@api_view(['POST'])
def Add_User1(request):
    data = request.data
    user = SingUpSerializer(data = data)

    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():   #l'unicité de l'email doit etre global 
            utlisateur = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'], 
                email = data['email'] , 
                username = data['email'] , 
                password = make_password(data['password']),
             
            )
            user1=User1.objects.create(user=utlisateur )
            return Response(
                {'details':'Your account User1 registered susccessfully!' },
                    status=status.HTTP_201_CREATED
                    )
        else:
            return Response(
                {'eroor':'This email already exists!' },
                    status=status.HTTP_400_BAD_REQUEST
                    )
    else:
        return Response(user.errors)


@api_view(['POST'])
def Add_User2(request):
    data = request.data
    user = SingUpSerializer(data = data)

    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():   #l'unicité de l'email doit etre global 
            utlisateur = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'], 
                email = data['email'] , 
                username = data['email'] , 
                password = make_password(data['password']),
             
            )
            user2=User2.objects.create(user=utlisateur )
            return Response(
                {'details':'Your account User2 registered susccessfully!' },
                    status=status.HTTP_201_CREATED
                    )
        else:
            return Response(
                {'eroor':'This email already exists!' },
                    status=status.HTTP_400_BAD_REQUEST
                    )
    else:
        return Response(user.errors)


@api_view(['POST'])
def Add_User3(request):
    data = request.data
    user = SingUpSerializer(data = data)

    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():   #l'unicité de l'email doit etre global 
            utlisateur = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'], 
                email = data['email'] , 
                username = data['email'] , 
                password = make_password(data['password']),
             
            )
            user1=User1.objects.create(user=utlisateur )
            return Response(
                {'details':'Your account User3 registered susccessfully!' },
                    status=status.HTTP_201_CREATED
                    )
        else:
            return Response(
                {'eroor':'This email already exists!' },
                    status=status.HTTP_400_BAD_REQUEST
                    )
    else:
        return Response(user.errors)



@api_view(['GET'])

def current_user(request):
    user = UserSerializer(request.user, many=False)
    return Response(user.data)



