from .views import ProjectViewSet, check_slug_view, add_member_view, post_project_update_view, leave_project_view
from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'projects'

router = DefaultRouter()
router.register('', ProjectViewSet, basename='projects')

urlpatterns = [
    path('check-slug/', check_slug_view, name="check_slug"),
    path('add-member/', add_member_view, name="add_member"),
    path('post-update/', post_project_update_view, name="project_post_update"),
    path('leave-project/', leave_project_view, name="leave_project")
]
urlpatterns += router.urls
