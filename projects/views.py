from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from projects.models import Project
from projects.serializers import ProjectSerializer


class ProjectsList(viewsets.ViewSet):
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
