from django.urls import path
from social.views import get_replies_view, post_reply_view, get_update_comments_view, post_update_comment_view, \
    notify_user_view, execute_notification_view

app_name = 'social'

urlpatterns = [
    path('get-comments/<int:comment_id>/', get_replies_view, name="get_comments"),
    path('post-reply/', post_reply_view, name="post_reply"),
    path('get-update-comments/<int:update_id>/', get_update_comments_view, name="get_update_comments"),
    path('post-update-comment/', post_update_comment_view, name="post_update_comment"),
    path('notify-user/', notify_user_view, name="notify_user"),
    path('execute-notification/', execute_notification_view, name="execute_notification")
]
