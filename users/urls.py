from django.urls import path
from .views import Account, accountView, HelloWorldView

app_name = 'users'

urlpatterns = [
    path('account/', accountView, name="create_user"),
    path('hello/', HelloWorldView.as_view(), name='hello_world')
]
