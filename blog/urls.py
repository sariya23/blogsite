from django.urls import path
from . import views
from .feeds import LatestPostsFeed


app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<int:year>/<int:month>/<int:day>/<slug:post_slug>/", views.post_detail, name="post_detail"),
    path("<int:post_pk>/share/", views.post_share, name="post_share"),
    path("<int:post_pk>/comment/", views.post_comment, name="post_comment"),
    path("tag/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),
    path("feed/", LatestPostsFeed(), name="feed"),
    path("search/", views.post_search, name="post_search"),
]