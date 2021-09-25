import json
from rest_framework import serializers

from projects.models import UserProject, Project
from users.models import User, Skill, UserSkill


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('name', 'id')


class UserSkillSerializer(serializers.ModelSerializer):

    skill = SkillSerializer()

    class Meta:
        model = UserSkill
        fields = ('skill', 'level')


class UserProjectSerializer(serializers.ModelSerializer):
    # user's version of the user-project serializer

    slug = serializers.CharField(source='project.slug', read_only=True)
    title = serializers.CharField(source='project.title', read_only=True)
    description = serializers.CharField(source='project.description', read_only=True)

    class Meta:
        model = UserProject
        fields = ('role', 'slug', 'title', 'description')


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    skills = UserSkillSerializer(many=True, source='skills_data', required=False)
    projects = UserProjectSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'username', 'bio', 'profile_pic', 'skills', 'projects')
        # so that we do not show the password, but can still post it
        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class MiniUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'username', 'profile_pic')
