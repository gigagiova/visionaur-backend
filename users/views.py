from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import UserSerializer


@authentication_classes([])
@permission_classes([AllowAny, ])
@api_view(['POST'])
def registerView(request):
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


class accountView(APIView):

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print(serializer)
            return Response(status=status.HTTP_200_OK)

        print(serializer.errors)
        return Response({'errors': serializer.errors})

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class HelloWorldView(APIView):

    def get(self, request):
        print(request.user)
        return Response(data={"hello": "world"}, status=status.HTTP_200_OK)
