from django.urls import path
from .views import registerView, loginView, accountView, checkUsernameView, SkillsList

app_name = 'users'

urlpatterns = [
    path('register/', registerView, name="register"),
    path('login/', loginView, name="login"),
    path('account/', accountView.as_view(), name="account"),
    path('check-username/', checkUsernameView, name='check_username'),
    path('skills/', SkillsList.as_view(), name='skills_list')
]
