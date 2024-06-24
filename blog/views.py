from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

from .models import Post
from .forms import EmailPostForm

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 1
    template_name = "blog/post/list.html"


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
    return render(request, "blog/post/detail.html", {"post": post})
