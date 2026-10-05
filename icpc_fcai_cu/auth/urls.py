from django.urls import path

from .views import *

app_name = "auth"

urlpatterns = [
    path('login', auth_view.login_view, name="login"),
    path('logout', auth_view.logout_view, name="logout"),
    # path('register/student', register_view.student, name="register-student"),
]
