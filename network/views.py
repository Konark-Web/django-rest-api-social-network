from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    posts = Post.objects.all().order_by('created_date')
    return render(request, 'post/post_list.html', {'posts': posts})


def post_single(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post/post_single.html', {'post': post})

