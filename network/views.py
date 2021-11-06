from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Subscribers
from .forms import SubscribeForm
from .tasks import send_email_to_user


def post_list(request):
    send_status = None
    form = SubscribeForm()

    if request.method == "POST":
        email = Subscribers.objects.filter(email=request.POST.get('email'))
        form = SubscribeForm(request.POST)
        if not email:
            if form.is_valid():
                form.save()
                send_email_to_user.delay(request.POST.get('email'))

                send_status = 'success'
            else:
                send_status = 'fail'
        else:
            send_status = 'already-exist'

    posts = Post.objects.all().order_by('-created_date')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'post/post_list.html', {'page_obj': page_obj, 'form': form, 'send_status': send_status})


def post_single(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post/post_single.html', {'post': post})

