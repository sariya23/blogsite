from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm


def post_list(request: HttpRequest, tag_slug=None) -> HttpResponse:
    post_all = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_all = post_all.filter(tags__in=[tag])

    paginator = Paginator(post_all, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post/list.html", {"posts": posts, "tag": tag})


def post_share(request: HttpRequest, post_pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=post_pk, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{clean_data['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {clean_data['name']} comments: {clean_data['comment']}"
            send_mail(subject, message, "account@gmail.com", [clean_data["recipient"]])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, "blog/post/share.html", {"post": post, "form": form, "sent": sent})


def post_detail(request: HttpRequest, year: int, month: int, day: int, post_slug: str) -> HttpResponse:
    post = get_object_or_404(Post,
                             slug=post_slug,
                             publish_date__year=year,
                             publish_date__month=month,
                             publish_date__day=day,
                             status=Post.Status.PUBLISHED,
                             )
    comments = post.comments.filter(active=Comment.Status.ACTIVE)
    form = CommentForm()

    post_tag_ids = post.tags.values_list('pk', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tag_ids).exclude(pk=post.pk)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by("-same_tags", "-publish_date")[:4]

    return render(request, "blog/post/detail.html",
                  {"post": post, "comments": comments, "form": form, "similar_posts": similar_posts})


@require_POST
def post_comment(request: HttpRequest, post_pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=post_pk, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(request, "blog/post/comment.html", {"post": post, "comment": comment, "form": form})


def post_search(request: HttpRequest) -> HttpResponse:
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = Post.published.annotate(
                similarity=TrigramSimilarity("title", query) + TrigramSimilarity("content", query)).filter(
                similarity__gte=0.1).order_by("-similarity")

    return render(request, "blog/post/search.html", {"form": form, "query": query, "results": results})
