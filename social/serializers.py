from rest_framework import serializers

from social.models import Comment, Update, Notification
from users.serializers import MiniUserSerializer


class CommentSerializer(serializers.ModelSerializer):

    by_user = MiniUserSerializer(required=False)
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ('children', )

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def get_children_count(self, obj):
        return obj.children.all().count()


class UpdateSerializer(serializers.ModelSerializer):

    by_user = MiniUserSerializer(required=False)

    class Meta:
        model = Update
        exclude = ('comments', )

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class NotificationSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(max_length=None, use_url=True, required=False, source='actor.profile_pic')
    actor_username = serializers.CharField(source='actor.username', read_only=True)

    class Meta:
        model = Notification
        fields = ('image', 'actor_username', 'verb', 'object_slug', 'completed', 'id', 'created')
