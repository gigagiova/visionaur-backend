from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from projects.models import Project
from projects.serializers import ProjectSerializer
from users.models import Skill
from rest_framework.decorators import api_view, permission_classes, authentication_classes


class ProjectViewSet(viewsets.ViewSet):
    queryset = Project.objects.all()
    lookup_field = 'slug'
    permission_classes = [AllowAny, ]
    authentication_classes = []

    def list(self, request):
        serializer = ProjectSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        project = get_object_or_404(self.queryset, slug=slug)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    def create(self, request):
        skills_list = request.data['skills_list']
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # this section saves the required skills, but in the future should be fixed
            project = Project.objects.get(slug=serializer.data['slug'])
            for skill in skills_list:
                project.skills_needed.add(Skill.objects.get(pk=skill))
            project.save()
            return Response(status=status.HTTP_200_OK)

        return Response({'errors': serializer.errors})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny, ])
def checkSlugView(request):
    return Response({'available': not Project.objects.filter(slug=request.data['slug']).exists()})