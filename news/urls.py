from django.urls import path
from news.views import PostDetailView, PostListView

app_name = "news"
urlpatterns = [
    path("", PostListView.as_view(), name="news"),
    path("<category_id>", PostListView.as_view(), name="news-by-category"),
    path("details/<slug:post_slug>", PostDetailView.as_view(), name="news-details")
]
