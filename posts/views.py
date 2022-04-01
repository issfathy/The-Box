# imports
import re
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy, reverse
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from .forms import NewPostForm, EditPostForm
from .models import Post
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
# Create your views here.

# view to like posts


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    messages.info(request, "Post Liked")
    return HttpResponse('Post Liked')


# view to see all published posts
def posts_home(request, topic_slug=None):
    object_list = Post.published.all()

    topic = None
    if topic_slug:
        topic = get_object_or_404(Tag, slug=topic_slug)
        object_list = object_list.filter(topics__in=[topic])

    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'posts/posts_home.html', {'posts': posts, 'page': page, 'topic': topic})


# view to see a particular post
@login_required
def post_detail(request, pk, slug):
    post = get_object_or_404(Post, pk=pk)

    # stuff = get_object_or_404(Post, id=self.kwargs['pk'])
    total_likes = post.total_likes
    # # context = {"total_likes": total_likes}

    return render(request, 'posts/post_detail.html', {'post': post})


# view to create a new post
@login_required
def new_post_view(request):
    swears = ["fuck", "shit", "bitch"]
    if request.method == 'POST':
        new_post_form = NewPostForm(request.POST, request.FILES)

        if new_post_form.is_valid():
            new_post = new_post_form.save(commit=False)
            new_post.author = request.user

            for i in swears:
                if(i in new_post.body or i in new_post.title):
                    return render(request, 'posts/new_post.html', {'new_post_form': new_post_form})

            new_post.save()
            topics = new_post_form.cleaned_data['topics']
            new_post.topics.add(*topics)

            new_post.save()

            return render(request, 'posts/draft_post.html', {'new_post': new_post})

    else:
        new_post_form = NewPostForm()

    return render(request, 'posts/new_post.html', {'new_post_form': new_post_form})


# view to edit a self post
@login_required
def edit_post(request, pk, slug):
    post = get_object_or_404(Post, pk=pk)
    if not request.user == post.author:
        return HttpResponseRedirect(reverse_lazy('posts:post_detail', args=[pk, slug]))

    if request.method == 'POST':
        edit_post_form = EditPostForm(request.POST)

        if edit_post_form.is_valid():
            swears = ["fuck", "shit", "bitch"]
            cd = edit_post_form.cleaned_data
            post.title = cd['title']
            post.body = cd['body']
            post.topics = cd['topics']

            for i in swears:
                if(i in cd['body'] or i in cd['title']):
                    return render(request, 'posts/edit_post.html', {'edit_post_form': edit_post_form})

            post.save()

            if post.status == 'draft':
                return render(request, 'posts/draft_post.html', {'new_post': post})
            else:
                return HttpResponseRedirect(reverse_lazy('posts:post_detail', args=[post.pk, post.slug]))

    else:
        edit_post_form = EditPostForm(data={'title': post.title,
                                            'body': post.body,
                                            'topics': []})

    return render(request, 'posts/edit_post.html', {'edit_post_form': edit_post_form})


# view to see all self draft posts
@login_required
def draft_posts(request):
    object_list = Post.drafts.filter(author=request.user)
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'posts/draft_posts.html', {'posts': posts, 'page': page})

# view to change status
@login_required
def status_page(request):

    return render(request, 'posts/status_page.html')

# view to see all topics
def topics_view(request):
    topics = Tag.objects.all()
    return render(request, 'posts/topics_page.html', {'topics': topics})
