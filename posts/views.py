from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model

from .forms import PostForm
from .models import Post, Group


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context ={
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context ={
        'page': page,
        'paginator': paginator,
        'group': group,
        'posts': posts,
    }
    return render(request, 'group.html', context)


def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'new.html', {'form': form})


def profile(request, username):
    profile = get_object_or_404(get_user_model(), username=username)
    post_list = profile.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    count_post = profile.posts.all().count()
    context = {
        "profile":profile,
        'page':page,
        'paginator':paginator,
        'count_post':count_post,
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    profile = get_object_or_404(get_user_model(), username=username)
    post = get_object_or_404(Post, id=post_id)
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'profile':profile,
        'post': post,
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'post.html', context)


def post_edit(request, username, post_id):
    author = get_object_or_404(get_user_model(), username=username)
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        edit = True
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect(post_view, username=post.author.username, post_id=post_id)
        form = PostForm(instance=post)
        context = {
            'form': form,
            'edit': edit,
            'post': post,
        }
        return render(request, 'new.html', context)
    return redirect(post_view, username=post.author.username, post_id=post_id)
