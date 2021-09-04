from .views import ProjectViewSet, checkSlugView
from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'projects'

router = DefaultRouter()
router.register('', ProjectViewSet, basename='projects')

urlpatterns = [
    path('check-slug/', checkSlugView, name="check_slug")
]
urlpatterns += router.urls
