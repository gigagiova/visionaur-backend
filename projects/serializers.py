from rest_framework import serializers
from projects.models import Project, UserProject
from social.serializers import UpdateSerializer
from users.serializers import SkillSerializer
from users.models import User, Skill


class UserProjectSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)
    profile_pic = serializers.ImageField(max_length=None, use_url=True, required=False, source='user.profile_pic')
    name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = UserProject
        fields = ('username', 'role', 'profile_pic', 'name')


class ProjectSerializer(serializers.ModelSerializer):

    skills_needed = SkillSerializer(many=True, required=False)
    team = UserProjectSerializer(many=True, source='members', required=False)
    image = serializers.ImageField(max_length=None, use_url=True, required=False)
    updates = UpdateSerializer(many=True, required=False)

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        proj = super().update(instance, validated_data)
        proj.save()
        return proj

    class Meta:
        model = Project
        fields = '__all__'
        lookup_field = 'slug'
