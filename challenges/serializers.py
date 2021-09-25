from rest_framework import serializers
from challenges.models import Challenge, ChallengeProject
from projects.models import Project
from social.serializers import CommentSerializer, UpdateSerializer
from users.serializers import MiniUserSerializer


class ChallengeProjectSerializer(serializers.ModelSerializer):

    slug = serializers.CharField(source='project.slug', read_only=True)
    title = serializers.CharField(source='project.title', read_only=True)
    description = serializers.CharField(source='project.description', read_only=True)

    class Meta:
        model = ChallengeProject
        fields = ('slug', 'winner', 'title', 'description')


class ChallengeSerializer(serializers.ModelSerializer):

    organizers = MiniUserSerializer(many=True, required=False)
    looking_for_team = MiniUserSerializer(many=True, required=False)
    image = serializers.ImageField(max_length=None, use_url=True, required=False)
    subscribed_projects = ChallengeProjectSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, required=False)
    updates = UpdateSerializer(many=True, required=False)

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.save()
        return instance

    class Meta:
        model = Challenge
        exclude = ('projects', )
        lookup_field = 'slug'
