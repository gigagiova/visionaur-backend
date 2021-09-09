from rest_framework import serializers
from projects.models import Project, UserProject
from users.serializers import SkillSerializer
from users.models import User, Skill


class UserProjectSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    image = serializers.ImageField(max_length=None, use_url=True, required=False, source='user.profile_pic')
    name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = UserProject
        fields = ('user', 'role', 'image', 'name')


class ProjectSerializer(serializers.ModelSerializer):

    skills_needed = SkillSerializer(many=True, required=False)
    team = UserProjectSerializer(many=True, source='members', required=False)
    image = serializers.ImageField(max_length=None, use_url=True, required=False)

    def create(self, validated_data):
        team = validated_data.pop('members', None)
        skills_needed = validated_data.pop('skills_needed', None)
        instance = self.Meta.model(**validated_data)
        instance.save()

        for member in team:
            UserProject.objects.create(user=User.objects.get(username=member['user']), project=instance, role=member['role'])
        
        return instance

    class Meta:
        model = Project
        fields = '__all__'
        lookup_field = 'slug'
