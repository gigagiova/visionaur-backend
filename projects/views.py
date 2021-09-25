from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from projects.models import Project, UserProject
from projects.serializers import ProjectSerializer, UserProjectSerializer
from social.models import Update
from social.serializers import UpdateSerializer
from users.models import Skill, User
from rest_framework.decorators import api_view, permission_classes, authentication_classes


class ProjectViewSet(viewsets.ViewSet):
    queryset = Project.objects.all()
    lookup_field = 'slug'

    @authentication_classes([])
    @permission_classes([AllowAny, ])
    def list(self, request):
        serializer = ProjectSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @authentication_classes([])
    @permission_classes([AllowAny, ])
    def retrieve(self, request, slug=None):
        project = get_object_or_404(self.queryset, slug=slug)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    def create(self, request):
        skills_list = request.data['skills_list']
        print(request.user)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # this section saves the required skills, but in the future should be fixed
            project = Project.objects.get(slug=serializer.data['slug'])
            UserProject.objects.create(
                user=request.user,
                project=project,
                role="F")
            project.skills_needed.set([Skill.objects.get(pk=skill) for skill in skills_list])
            project.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'errors': serializer.errors})

    def update(self, request, slug=None):
        project = self.queryset.get(slug=slug)
        # check if user has the right permissions
        if project.user_role(request.user) not in ['F', 'A']:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        skills_list = request.data['skills_list']
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # this section adds and deletes the required skills, but in the future should be fixed
            new_list = [Skill.objects.get(pk=skill) for skill in skills_list]
            project.skills_needed.set(new_list, clear=True)
            project.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'errors': serializer.errors})

    def destroy(self, request, slug=None):
        project = self.queryset.get(slug=slug)
        if project.user_role(request.user) == "F":
            # only the founder can delete a project
            project.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def add_member_view(request):
    project = Project.objects.get(slug=request.data["slug"])
    new_user = User.objects.filter(username=request.data["user"]).first()
    if project.user_Role is not None and new_user is not None:
        if project.team.filter(username=new_user).exists():
            return Response({'error': 'user already member'}, status=status.HTTP_400_BAD_REQUEST)
        # if the requesting user is part of the team and the new user is valid and not already member
        membership = UserProject.objects.create(user=new_user, project=project)
        return Response(UserProjectSerializer(membership).data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny, ])
def check_slug_view(request):
    return Response({'available': not Project.objects.filter(slug=request.data['slug']).exists()})


@api_view(['POST'])
def post_project_update_view(request):
    try:
        project = Project.objects.get(slug=request.data['slug'])
        if project.user_role(request.user) is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        update = Update(text=request.data['text'], by_user=request.user)
        update.save()
        project.updates.add(update)
        project.save()
        return Response(UpdateSerializer(update).data, status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def leave_project_view(request):
    try:
        project = Project.objects.get(slug=request.data['slug'])
        UserProject.objects.filter(project=project, user=request.user).delete()
        return Response(status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
