# imports
from concurrent.futures import thread
from sre_constants import SUCCESS
from django import forms
from django.dispatch import receiver
from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views import View
from flask import redirect
from .forms import UserRegistrationForm, UserProfileForm, LoginForm, EditProfileForm, DeleteProfileForm, ThreadForm, MessageForm
from .models import ThreadModel, UserProfile, ThreadModel, MessageModel
from django.contrib import messages
from django.db.models import Q
# from django.db.models import Q

# Create your views here.

# new user registration view


def register(request):
    # logout required for registration
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('homepage'))

    # if form filled
    if request.method == 'POST':
        user_form = UserRegistrationForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_profile = profile_form.save(commit=False)

            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()

            new_profile.user = new_user
            new_profile.save()

            # login

            return HttpResponse("Account Created")
    # if new form to be rendered
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'accounts/register.html', context={'user_form': user_form, 'profile_form': profile_form})


# login view
def login_view(request):
    # logout required for login
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('homepage'))

    # if form filled
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)

        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    next_page = request.GET.get('next')

                    if next_page:
                        return HttpResponseRedirect(next_page)

                    return HttpResponseRedirect(reverse_lazy('homepage'))

                else:
                    return HttpResponse("Account Terminated!")

            else:
                return HttpResponse("User Doesnt exist!")

    # if new form is to be rendered
    else:
        login_form = LoginForm()

    return render(request, 'accounts/login.html', context={'login_form': login_form})


# view someone's profile
@login_required
def profile_view(request, username):

    user = get_object_or_404(User, username=username)

    # check if the current user follows this user
    follow = False
    try:
        if request.user.profile.following.get(user=user):
            follow = True
    except Exception as e:
        print(e)

    return render(request, 'accounts/profile_page.html', {'user': user, 'follow': follow})


@login_required
def mute_view(request, username):
    user = get_object_or_404(User, username=username)
    # check if the current user follows this user
    follow = False
    try:
        if request.user.profile.following.get(user=user):
            follow = True
    except Exception as e:
        print(e)

    return render(request, 'accounts/profile_hidden.html', {'user': user, 'follow': follow})

# view to edit self profile


@login_required
def edit_profile_view(request, username):
    # to handle attempts to edit someone else's profile
    user = request.user.profile
    form = EditProfileForm(instance=user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/edit_profile.html', context)


# view to delete profile
def delete_event(request, username):

    delete_form = DeleteProfileForm(
        request.POST, request.FILES, instance=request.user)
    user = request.user
    user.delete()
    messages.info(request, 'Your account has been deleted.')
    return HttpResponse('ACCOUNT DELETED')


# view to follow someone
@login_required
def follow_view(request, username):
    # to prevent following self
    if username == request.user.username:
        return HttpResponseRedirect(reverse_lazy('accounts:profile', args=[username]))

    user_to_follow = get_object_or_404(User, username=username)
    current_user = request.user

    current_user.profile.following.add(user_to_follow.profile)

    current_user.save()

    return HttpResponseRedirect(reverse_lazy('accounts:profile', kwargs={'username': username}))

# view to unfollow someone


@login_required
def block_view(request, username):
    return HttpResponse('ACCOUNT MUTED')

# view to unfollow someone


@login_required
def unfollow_view(request, username):
    # to prevent unfollowing self
    if username == request.user.username:
        return HttpResponseRedirect(reverse_lazy('accounts:profile', args=[username]))

    user_to_unfollow = get_object_or_404(User, username=username)
    current_user = request.user

    try:
        if current_user.profile.following.get(user=user_to_unfollow):
            current_user.profile.following.remove(user_to_unfollow.profile)
            current_user.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(reverse_lazy('accounts:profile', kwargs={'username': username}))


# showing suggested people to follow
@login_required
def accounts_home(request):

    suggested_users = User.objects.exclude(
        profile__followers__user__username__contains=request.user.username
    )

    users = request.user.profile.following.all()

    users = User.objects.filter(
        profile__following__user__username__contains=request.user.username)

    type_of_users = "Suggested Users"

    return render(request, 'accounts/home.html', {'users': suggested_users, 'type_of_users': type_of_users})


# showing followers
@login_required
def followers(request):

    follower_users = User.objects.filter(
        profile__following__user__username__contains=request.user.username)

    type_of_users = "Followers"

    return render(request, 'accounts/home.html', {'users': follower_users, 'type_of_users': type_of_users})


# showing followed people
@login_required
def following(request):

    following_users = request.user.profile.following.all()

    type_of_users = "Following"

    return render(request, 'accounts/home.html', {'users': following_users, 'type_of_users': type_of_users})


class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(
            Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }

        return render(request, 'accounts/inbox.html', context)


class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }
        return render(request, 'accounts/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = User.objects.get(username=username)

            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(
                    user=request.user, receiver=receiver)[0]
                return HttpResponse('Thread Already Created')
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(
                    user=receiver, receiver=request.user)[0]
                return HttpResponse('Thread Already Created')

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return HttpResponse('Thread Created')
        except:
            return HttpResponse('Thread Created')


class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }

        return render(request, 'accounts/thread.html', context)


class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('message')
        )

        message.save()
        return HttpResponse("Message Sent")
