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
        fields = ('email', 'password', 'first_name', 'last_name', 'username', 'bio', 'profile_pic', 'skills')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        username = f'{instance.first_name}.{instance.last_name}'
        username.replace(' ', '')
        counter = 1
        while User.objects.filter(username=username):
            username += str(counter)
            counter += 1
        instance.username = username

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

