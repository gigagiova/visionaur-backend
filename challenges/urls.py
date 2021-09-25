from .views import ChallengeViewSet, check_slug_view, add_member_view, submit_project_view, toggle_waiting_view, \
    post_challenge_comment_view, post_challenge_update_view
from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'challenges'

router = DefaultRouter()
router.register('', ChallengeViewSet, basename='challenges')

urlpatterns = [
    path('check-slug/', check_slug_view, name="check_slug"),
    path('add-member/', add_member_view, name="challenge_add_member"),
    path('submit-project/', submit_project_view, name="submit_project"),
    path('toggle-waiting/', toggle_waiting_view, name="toggle-waiting"),
    path('post-comment/', post_challenge_comment_view, name="challenge_post_comment"),
    path('post-update/', post_challenge_update_view, name="challenge_post_update")
]
urlpatterns += router.urls
