from rest_framework import serializers
from projects.models import Project, UserProject
from users.serializers import SkillSerializer, MiniUserSerializer


class UserProjectSerializer(serializers.ModelSerializer):

    user = MiniUserSerializer()

    class Meta:
        model = UserProject
        fields = ('user', 'role')


class ProjectSerializer(serializers.ModelSerializer):

    skills_needed = SkillSerializer(many=True, required=False)
    team = UserProjectSerializer(many=True, source='members', required=False)
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Project
        fields = '__all__'
        lookup_field = 'slug'
