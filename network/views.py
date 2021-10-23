from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post


def post_list(request):
    posts = Post.objects.all().order_by('-created_date')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'post/post_list.html', {'page_obj': page_obj})


def post_single(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post/post_single.html', {'post': post})

