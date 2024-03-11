from django.urls import path

from .views import (
    DashboardView,
    BloodGroupsView,
    DonationListView,
    DonationDetailView,
    DonationCreateView,
    DonationEditView,
    DonationDeleteView,
)

# General Urls
general_urls = [
    path(
        "dashboard/",
        DashboardView.as_view(),
        name="dashboard",
    ),
    path(
        "bloodgroups/",
        BloodGroupsView.as_view(),
        name="bloodgroups",
    ),
]


# Donation Urls
donation_urls = [
    path(
        "donations/",
        DonationListView.as_view(),
        name="donation-list",
    ),
    path(
        "donations/new/",
        DonationCreateView.as_view(),
        name="donation-new",
    ),
    path(
        "donations/<int:pk>/",
        DonationDetailView.as_view(),
        name="donation-detail",
    ),
    path(
        "donations/edit/<int:pk>/",
        DonationEditView.as_view(),
        name="donation-edit",
    ),
    path(
        "donations/delete/<int:pk>/",
        DonationDeleteView.as_view(),
        name="donation-delete",
    ),
]


# All
urlpatterns = general_urls + donation_urls
