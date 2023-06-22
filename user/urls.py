"""
URL mappings for user API
"""

from django.urls import path

from user import views

app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserModel.as_view(), name="create"),
]
