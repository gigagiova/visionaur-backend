import json

from django.shortcuts import get_object_or_404

from users import auth
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User, Skill, UserSkill
from users.serializers import UserSerializer, SkillSerializer


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = [AllowAny, ]
    authentication_classes = []

    def list(self, request):
        serializer = UserSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, username=None):
        user = get_object_or_404(self.queryset, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny, ])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        new_user = serializer.save()
        print(new_user)
        if new_user:
            refresh = RefreshToken.for_user(new_user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                **serializer.data
            }, status=status.HTTP_201_CREATED)

    # error handling
    if 'email' in serializer.errors:
        return Response({'error': 'email_taken'})

    return Response({'error': 'generic'})


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

        user_skills = UserSkill.objects.filter(user=request.user)
        loaded_skills = json.loads(request.data['stringified_skills'])

        # this block removes the skills we have not included in the last version
        # it is placed before the block that adds new skills, because otherwise we delete what we add
        for u in user_skills.all():
            still_contained = False
            for s in loaded_skills:
                if s['skill']['id'] == u.id:
                    # if we found the skill in the upcoming data we keep the skill
                    still_contained = True
            if not still_contained:
                # we delete the skill if it is not present in the new version
                u.delete()

        # check if there are any new skills to add
        for s in loaded_skills:
            if not user_skills.filter(skill_id=s['skill']['id']).exists():
                UserSkill.objects.create(user=request.user, skill_id=s["skill"]["id"], level=s["level"])

        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'errors': serializer.errors})

    def get(self, request):
        return Response(UserSerializer(request.user).data)


@api_view(['POST'])
@authentication_classes([auth.JWTAuthenticationSafe])
@permission_classes([AllowAny, ])
def checkUsernameView(request):
    print(request.user)
    if request.user.username == request.data['username']:
        # our own username is available by definition
        return Response({'available': True})
    return Response({'available': not User.objects.filter(username=request.data['username']).exists()})


class SkillsList(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer