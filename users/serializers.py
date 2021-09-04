import json

from rest_framework import serializers
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


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    skills = UserSkillSerializer(many=True, source='skills_data', required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'username', 'bio', 'profile_pic', 'skills')

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
