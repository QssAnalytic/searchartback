from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from .serializers import UserRegistrationSerializer, UserLoginSerializer

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

@api_view(['POST'])
@permission_classes((AllowAny,))
def login_api(request):
    login_data = JSONParser().parse(request)
    serializer = UserLoginSerializer(data=login_data)
    print(type(serializer))
    if serializer.is_valid():
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user:
            token,created = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key},status=201)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



