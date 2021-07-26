from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserSerializer


class Account(APIView):
    permission_classes = [AllowAny, ]
    authentication_classes = ()

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            if new_user:
                refresh = RefreshToken.for_user(new_user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'first_name': new_user.first_name,
                    'last_name': new_user.last_name,
                    'email': new_user.email
                }, status=status.HTTP_201_CREATED)

        # error handling
        if serializer['email']:
            return Response({'error': 'email_taken'})

        return Response({'errors': serializer.errors})


@api_view(['GET', 'PUT'])
def accountView(request):
    print(request.data)
    print(request.user)
    return Response(status=status.HTTP_200_OK)


class HelloWorldView(APIView):

    def get(self, request):
        print(request.user)
        return Response(data={"hello": "world"}, status=status.HTTP_200_OK)
