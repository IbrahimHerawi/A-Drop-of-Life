from django.urls import path


from .views import (
    HomePageView,
    AboutusPageView,
    QuestionsPageView,
)


urlpatterns = [
    path("home/", HomePageView.as_view(), name="home"),
    path("aboutus/", AboutusPageView.as_view(), name="aboutus"),
    path("questions/", QuestionsPageView.as_view(), name="questions"),
]
