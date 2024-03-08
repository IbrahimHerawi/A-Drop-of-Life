from django.urls import path

from .views import (
    DashboardView,
    BloodGroupsView,
)


urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("bloodgroups/", BloodGroupsView.as_view(), name="bloodgroups"),
]
