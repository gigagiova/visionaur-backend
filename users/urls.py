from django.urls import path
from .views import registerView, accountView, HelloWorldView

app_name = 'users'

urlpatterns = [
    path('register/', registerView, name="register"),
    path('account/', accountView.as_view(), name="account"),
    path('hello/', HelloWorldView.as_view(), name='hello_world')
]
