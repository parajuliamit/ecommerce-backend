from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

from base.serializers import UserSerializer, UserSerializerWithToken, RegisterUserSerializer



class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        return serializer

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

@api_view(['POST'])
def registerUser(request):
    data = request.data
    resgister_serializer = RegisterUserSerializer(data=data)
    if resgister_serializer.is_valid():
        try:
            user = User.objects.create(
                first_name = data['name'],
                username = data ['email'],
                email = data ['email'],
                password=make_password(data['password'])
            )
            user.save()
            serializer = UserSerializerWithToken(user,many = False)
            return Response(serializer.data)
        except Exception as e:
            print (e)
            message = {'detail':'User with this email already exists.'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(resgister_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user,many = False)
    return Response(serializer.data)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializer(user,many = False)

    data = request.data

    if 'name' in data:
        user.first_name = data['name']
    
    if 'email' in data:
        user.email = data['email']
        user.username = data['email']
    
    user.save()
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def changePassword(request):
    user = request.user
    serializer = UserSerializer(user,many = False)

    data = request.data
    
    if 'password' in data:
        user.password = make_password(data['password'])
    
    user.save()
    return Response(serializer.data)