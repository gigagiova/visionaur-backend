from django.urls import path
from .views import CreateUser, HelloWorldView

app_name = 'users'

urlpatterns = [
    path('register/', CreateUser.as_view(), name="create_user"),
    path('hello/', HelloWorldView.as_view(), name='hello_world')
]
