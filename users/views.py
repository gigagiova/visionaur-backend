import json
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from users.serializers import UserSerializer


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny, ])
def registerView(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        new_user = serializer.save()
        if new_user:
            refresh = RefreshToken.for_user(new_user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                **serializer.data
            }, status=status.HTTP_201_CREATED)

    # error handling
    if serializer['email']:
        return Response({'error': 'email_taken'})

    return Response({'errors': serializer.errors})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny, ])
def loginView(request):
    body = json.loads(request.body)
    try:
        user = User.objects.get(email=body['email'])
    except BaseException as e:
        return Response({'error': str(e)})

    if not check_password(body['password'], user.password):
        return Response({'error': 'Incorrect Login credentials'})

    if user:
        login(request, user)
        refresh = RefreshToken.for_user(user)

        print({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            **UserSerializer(user).data
        })

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            **UserSerializer(user).data
        }, status=status.HTTP_200_OK)

    else:
        return Response({'error': 'Account doesnt exist'})


class accountView(APIView):

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)

        print(serializer.errors)
        return Response({'errors': serializer.errors})

    def get(self, request):
        return Response(UserSerializer(request.user).data)


@api_view(['POST'])
def checkUsernameView(request):
    if request.user.username == request.data['username']:
        # our own username is available by definition
        return Response({'available': True})
    return Response({'available': not User.objects.filter(username=request.data['username']).exists()})
