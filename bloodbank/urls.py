from django.urls import path

from .views import (
    # General Views
    DashboardView,
    BloodGroupsView,
    # Donor Views
    DonorCreateView,
    DonorEditView,
    DonorDeleteView,
    # Donation Views
    DonationListView,
    DonationCreateView,
    DonationDetailView,
    DonationEditView,
    DonationDeleteView,
    # Request Views
    RequestListView,
    RequestCreateView,
    RequestDetailView,
    RequestEditView,
    RequestDeleteView,
    StateMaintainingView,
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


# Donor Urls
donor_urls = [
    path(
        "donor/new/",
        DonorCreateView.as_view(),
        name="donor-new",
    ),
    path(
        "donor/edit/<int:pk>/",
        DonorEditView.as_view(),
        name="donor-edit",
    ),
    path(
        "donor/delete/<int:pk>/",
        DonorDeleteView.as_view(),
        name="donor-delete",
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


# Request Urls
request_urls = [
    path(
        "requests/",
        RequestListView.as_view(),
        name="request-list",
    ),
    path(
        "requests/new/",
        RequestCreateView.as_view(),
        name="request-new",
    ),
    path(
        "requests/<int:pk>/",
        RequestDetailView.as_view(),
        name="request-detail",
    ),
    path(
        "requests/edit/<int:pk>/",
        RequestEditView.as_view(),
        name="request-edit",
    ),
    path(
        "requests/delete/<int:pk>/",
        RequestDeleteView.as_view(),
        name="request-delete",
    ),
    path(
        "requests/statemaintaining/",
        StateMaintainingView,
        name="state-maintaining",
    ),
]


# All
urlpatterns = general_urls + donor_urls + donation_urls + request_urls
