from .views import ProjectsList
from rest_framework.routers import DefaultRouter

app_name = 'projects'

router = DefaultRouter()
router.register('', ProjectsList, basename='projects')

urlpatterns = []
urlpatterns += router.urls
