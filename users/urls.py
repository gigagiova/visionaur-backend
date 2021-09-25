from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import register_view, login_view, AccountView, check_username_view, SkillsList, UserViewSet, \
    get_notifications_view

app_name = 'users'

router = DefaultRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('my-account/', AccountView.as_view(), name="account"),
    path('check-username/', check_username_view, name='check_username'),
    path('get-notifications/', get_notifications_view, name="get_notifications"),
    path('skills/', SkillsList.as_view(), name='skills_list')
]

urlpatterns += router.urls
