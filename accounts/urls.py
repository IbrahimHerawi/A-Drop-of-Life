from django.urls import path

from .views import UserEditView


urlpatterns = [
    path("profile/<uuid:pk>/", UserEditView.as_view(), name="profile"),
]
