from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from projects.models import Project, UserProject
from social.models import Comment, Update, Notification
from social.serializers import CommentSerializer
from users.models import User


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny, ])
def get_replies_view(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        serializer = CommentSerializer(comment.children, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def post_reply_view(request):
    try:
        comment = Comment.objects.get(id=request.data['comment_id'])
        reply = Comment(text=request.data['text'], by_user=request.user)
        reply.save()
        comment.children.add(reply)
        comment.save()
        return Response(CommentSerializer(comment.children, many=True).data, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_update_comments_view(request, update_id):
    try:
        update = Update.objects.get(id=update_id)
        serializer = CommentSerializer(update.comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def post_update_comment_view(request):
    try:
        update = Update.objects.get(id=request.data['id'])
        comment = Comment(text=request.data['text'], by_user=request.user)
        comment.save()
        update.comments.add(comment)
        update.save()
        return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def notify_user_view(request):
    try:
        notification = Notification(actor=request.user, verb=request.data['verb'], object_slug=request.data['slug'])
        notification.save()
        target = User.objects.get(username=request.data['target'])
        target.notifications.add(notification)
        target.save()
        return Response(status=status.HTTP_200_OK)
    except (KeyError, User.DoesNotExist):
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def execute_notification_view(request):
    # executes the possible action contained in a notification
    notification = Notification.objects.get(id=request.data['id'])

    if notification.completed:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if notification.verb == Notification.Verbs.INVITE_TO_PROJECT:
        project = Project.objects.get(slug=notification.object_slug)
        UserProject.objects.create(user=request.user, project=project)
        notification.completed = True
        notification.save()
        return Response(status=status.HTTP_200_OK)
