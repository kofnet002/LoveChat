from django.shortcuts import redirect, render
from .models import LikePost, User, Post, Follow, Comment
from .forms import MyUserCreationForm,UserAuthenticationForm, UpdateUserForm, PostFeedForm
from django.contrib import messages
from chat.models import ChatMessage
from groupChat.models import Room
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
from django.db.models import Q
from django.http import HttpResponse


def registerPage(request):
    form = MyUserCreationForm()
    if request.user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {request.user.email}")
    
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

             # clean user intput & login user
            username = form.cleaned_data.get('username').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)

            messages.info(request, "Accounted Created Successfully")
            return redirect('home')
        else:
            messages.info(request, "Something went wrong")

    context = {
        'registration_form': form
    }
    return render(request, 'base/register.html', context)


def loginPage(request):
    form = UserAuthenticationForm()

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')
    context = {
    'login_form': form
    }  
    return render(request, 'base/login.html', context)


@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profilePage(request, pk):
    user = User.objects.get(username=pk)
    posts = Post.objects.filter(host=user)
    posts_length = posts.count()
    form = UpdateUserForm(instance=user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.info(request, "Profile Updated Successfully!")
            return redirect('/user-profile/' + request.user.username)
            # return redirect('/user-profiel/'+user)

    follower = request.user.username
    follow_filter = Follow.objects.filter(follower=follower, user=pk).first()
    if follow_filter:
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    # Users the authenticated user followers
    users_following = Follow.objects.filter(follower=pk).count()
    # Users that follow the authenticated user
    users_follower = Follow.objects.filter(user=pk).count()

    context = {
        'form': form,
        'posts': posts,
        'posts_length': posts_length,
        'user': user,
        'button_text': button_text,
        'users_following': users_following,
        'users_follower': users_follower,
    }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def home(request):
    # Getting the username of the users you follow
    user_following_list = []
    feed = []
    user_following = Follow.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    # Using the username above to help get the queryset or objectes
    new_user_following_list = []
    for i in user_following_list:
        x1 = User.objects.get(username=i)
        new_user_following_list.append(x1)
    

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(host__username=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    username = request.user.username
    post_id = request.GET.get('post_id')

    like_filter = LikePost.objects.filter(
        post_id=post_id, username=username).first()

    # MESSAGES DISPLAY
    chat_messages = ChatMessage.get_message(user=request.user)

    # ROOMS
    rooms = Room.objects.all()

    # User suggestions
    all_users = User.objects.all()
    user_following_all = []
    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users)
                            if (x not in list(user_following_all))]

    current_user = User.objects.filter(username=request.user.username)

    final_suggestions_list = [x for x in list(
        new_suggestions_list) if (x not in list(current_user))]

    random.shuffle(final_suggestions_list)

    context = {
        'posts': feed_list,
        'suggest_users': final_suggestions_list[:3],
        # 'user_following': user_following[:20],
        'chat_messages': chat_messages[:3],
        'rooms': rooms[:5],
        'like_filter': like_filter,
        'follows':new_user_following_list[-3:],
    }
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def search(request):
    q = request.GET.get('q')

    user = User.objects.filter(
            Q(name__icontains=q) |
            Q(username__icontains=q) 
        )

    room = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
    )

    # post = Post.objects.filter(
    #     Q(host__icontains=q) |
    #     Q(caption__icontains=q) 
    # )

    context = {
        # 'posts': post, 
        'users': user,
        'rooms':room,
    }
    return render(request, 'base/search.html', context)


@login_required(login_url='login')
def post(request):
    form = PostFeedForm()
    if request.method == 'POST':
        form = PostFeedForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.host = request.user
            post.save()
            messages.info(request, "Posted Successfully!")
            return redirect('home')

    context = {
        'form': form
    }
    return render(request, 'base/post.html', context)


@login_required(login_url='login')
def post_detail(request, pk):
    posts = Post.objects.get(caption=pk)
    comments = Comment.objects.filter(post_id=posts.id)

    if request.method == 'POST':
        post = posts
        user = request.user
        body = request.POST.get('comment')
        comment = Comment.objects.create(post=post, user=user, body=body)
        comment.save()

    context = {
        'post_details': posts,
        'comments': comments,
    }

    return render(request, 'base/post_detail.html', context)


@ login_required(login_url='login')
def likePost(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(
        post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()

        post.no_of_likes += 1
        post.save()
        return redirect('home')
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect('home')


@ login_required(login_url='login')
def update_post(request, pk):
    post = Post.objects.get(id=pk)
    form = PostFeedForm(instance=post)
    if request.method == 'POST':
        form = PostFeedForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.info(request, "Updated sucessfully!")
            return redirect('home')

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'base/update_post.html', context)


@ login_required(login_url='login')
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    messages.info(request, "Deleted successfully!")
    return redirect('/user-profile/' + request.user.username)
    context = {
        # 'form': form
    }

    return render(request, 'base/home.html', context)


@ login_required(login_url='login')
def follow(request):
    follower = request.user.username
    user = request.GET.get('user')

    follow_filter = Follow.objects.filter(follower=follower, user=user).first()

    if follow_filter == None:
        new_follow = Follow.objects.create(follower=follower, user=user)
        new_follow.save()
        return redirect('/user-profile/'+user)
    else:
        follow_filter.delete()
        return redirect('/user-profile/'+user)


@ login_required(login_url='login')
def medium_follow(request):
    # Getting the username of the users you follow
    user_following_list = []
    feed = []
    user_following = Follow.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    # Using the username above to help get the queryset or objectes
    new_user_following_list = []
    for i in user_following_list:
        x1 = User.objects.get(username=i)
        new_user_following_list.append(x1)

    context = {
        'user_following': new_user_following_list,
    }
    return render(request, 'base/following.html', context)


@ login_required(login_url='login')
def medium_suggestion(request):
    # User suggestions
    user_following = Follow.objects.filter(follower=request.user.username)
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users)
                            if (x not in list(user_following_all))]

    current_user = User.objects.filter(username=request.user.username)

    final_suggestions_list = [x for x in list(
        new_suggestions_list) if (x not in list(current_user))]

    # final_suggestions_list = list(chain(*final_suggestions_list))
    random.shuffle(final_suggestions_list)
    context = {
        'suggest_users': final_suggestions_list[:20],

    }
    return render(request, 'base/suggestion.html', context)
