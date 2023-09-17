from django.urls import path
from home.views import HomeView, EmailTemplateView, SearchView

app_name = "home"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("email", EmailTemplateView.as_view(), name="email"),
    path("search", SearchView.as_view(), name="search-results"),
]
