from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from challenges.models import Challenge
from challenges.serializers import ChallengeSerializer
from projects.models import Project
from social.models import Comment, Update
from social.serializers import CommentSerializer, UpdateSerializer
from users.models import User
from users.serializers import MiniUserSerializer


class ChallengeViewSet(viewsets.ViewSet):
    queryset = Challenge.objects.all()
    serializer = ChallengeSerializer
    lookup_field = 'slug'

    @authentication_classes([])
    @permission_classes([AllowAny, ])
    def list(self, request):
        serializer = self.serializer(self.queryset, many=True)
        return Response(serializer.data)

    @authentication_classes([])
    @permission_classes([AllowAny, ])
    def retrieve(self, request, slug=None):
        project = get_object_or_404(self.queryset, slug=slug)
        serializer = self.serializer(project)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.queryset.get(slug=serializer.data['slug']).organizers.add(request.user)
            # this section saves the required skills, but in the future should be fixed
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'errors': serializer.errors})

    def update(self, request, slug=None):
        challenge = self.queryset.get(slug=slug)
        # check if user is an organizer
        if not challenge.organizers.filter(username=request.user.username).exists():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.serializer(challenge, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'errors': serializer.errors})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny, ])
def check_slug_view(request):
    return Response({'available': not Challenge.objects.filter(slug=request.data['slug']).exists()})


@api_view(['POST'])
def add_member_view(request):
    challenge = Challenge.objects.get(slug=request.data["slug"])
    new_user = User.objects.filter(username=request.data["user"]).first()
    if challenge.organizers.filter(username=request.user.username).exists():
        if challenge.organizers.filter(username=new_user).exists():
            return Response({'error': 'user already organizer'}, status=status.HTTP_400_BAD_REQUEST)
        # if the requesting user is part of the team and the new user is valid and not already member
        challenge.organizers.add(new_user)
        return Response(MiniUserSerializer(new_user).data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def submit_project_view(request):
    print(request)
    project = Project.objects.filter(slug=request.data["project_slug"]).first()
    challenge = Challenge.objects.filter(slug=request.data["challenge_slug"]).first()

    if project is None or challenge is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if project.user_role(request.user) not in ['F', 'A']:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if challenge.projects.filter(slug=request.data["project_slug"]).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    challenge.projects.add(project)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def toggle_waiting_view(request):
    challenge = Challenge.objects.filter(slug=request.data["challenge_slug"]).first()

    if challenge is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.user in challenge.looking_for_team.all():
        challenge.looking_for_team.remove(request.user)
    else:
        challenge.looking_for_team.add(request.user)

    return Response(MiniUserSerializer(challenge.looking_for_team, many=True).data, status=status.HTTP_200_OK)


@api_view(['POST'])
def post_challenge_comment_view(request):
    try:
        challenge = Challenge.objects.get(slug=request.data['slug'])
        comment = Comment(text=request.data['text'], by_user=request.user)
        comment.save()
        challenge.comments.add(comment)
        challenge.save()
        return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def post_challenge_update_view(request):
    try:
        challenge = Challenge.objects.get(slug=request.data['slug'])
        if not challenge.organizers.filter(username=request.user.username).exists():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        update = Update(text=request.data['text'], by_user=request.user)
        update.save()
        challenge.updates.add(update)
        challenge.save()
        return Response(UpdateSerializer(update).data, status=status.HTTP_200_OK)
    except Challenge.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
