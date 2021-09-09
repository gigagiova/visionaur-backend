from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import register_view, loginView, accountView, checkUsernameView, SkillsList, UserViewSet

app_name = 'users'

router = DefaultRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('register/', register_view, name="register"),
    path('login/', loginView, name="login"),
    path('my-account/', accountView.as_view(), name="account"),
    path('check-username/', checkUsernameView, name='check_username'),
    path('skills/', SkillsList.as_view(), name='skills_list')
]

urlpatterns += router.urls
