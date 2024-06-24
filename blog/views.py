from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post


def post_list(request: HttpRequest) -> HttpResponse:
    posts_list = Post.published.all()
    paginator = Paginator(posts_list, 1)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request: HttpRequest, year: int, month: int, day: int, post_slug: str) -> HttpResponse:
    post = get_object_or_404(Post,
                             slug=post_slug,
                             publish_date__year=year,
                             publish_date__month=month,
                             publish_date__day=day,
                             status=Post.Status.PUBLISHED,
                             )
    return render(request, "blog/post/detail.html", {"post": post})
