from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, Followers
from itertools import chain
import random

# Create your views here.


@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = Followers.objects.filter(
        follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for user_name in user_following_list:
        feed_lists = Post.objects.filter(user=user_name)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # user following suggestions of users that are not the currently logged in user or already followed
    all_users = User.objects.all()
    user_is_following = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_is_following.append(user_list)

    new_suggestions_list = [x for x in list(
        all_users) if (x not in list(user_is_following))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions = [x for x in list(
        new_suggestions_list) if (x not in list(current_user))]
    
    random.shuffle(final_suggestions)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_profiles = list(chain(*username_profile_list))

    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed_list, 'suggestions_profiles': suggestions_profiles[:6]})


# pk is the username of the currently viewed user
@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_number_of_posts = len(user_posts)
    follower = request.user.username
    user = pk

    if Followers.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_number_of_followers = len(Followers.objects.filter(user=pk))
    user_number_of_following = len(Followers.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_number_of_posts': user_number_of_posts,
        'button_text': button_text,
        'user_number_of_followers': user_number_of_followers,
        'user_number_of_following': user_number_of_following,
    }

    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST' and request.FILES.get('image_upload') != None:
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)
    # check if this post is already liked by the current user
    like_filter = LikePost.objects.filter(
        post_id=post_id, username=username).first()

    if like_filter == None:
        # like post
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.number_of_likes = post.number_of_likes + 1
        post.save()
        return redirect('/')
    else:
        # the post is already liked, remove like
        like_filter.delete()
        post.number_of_likes = post.number_of_likes - 1
        post.save()
        return redirect('/')


@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

    username_profile = []
    username_profile_list = []

    for users in username_object:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    username_profile_list = list(chain(*username_profile_list))

    context = {
        'user_profile': user_profile,
        'username_profile_list': username_profile_list,
        'username_profile_list_len': len(username_profile_list)
    }

    return render(request, 'search.html', context)


@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        # the follower is already following the user -> unfollow the user
        if Followers.objects.filter(follower=follower, user=user).first():
            delete_follower = Followers.objects.get(
                follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            # follow the user
            new_follower = Followers.objects.create(
                follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
        elif request.FILES.get('image') != None:
            image = request.FILES.get('image')

        bio = request.POST['bio']
        location = request.POST['location']
        phone_number = request.POST['phone_number']

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.phone_number = phone_number
        user_profile.save()
        return redirect('settings')
    return render(request, 'settings.html', {'user_profile': user_profile})


@login_required(login_url='signin')
def myposts(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=user_object)
    user_number_of_posts = len(user_posts)

    user_number_of_followers = len(Followers.objects.filter(user=user_object))
    user_number_of_following = len(Followers.objects.filter(follower=user_object))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_number_of_posts': user_number_of_posts,
        'user_number_of_followers': user_number_of_followers,
        'user_number_of_following': user_number_of_following,
    }

    return render(request, 'myposts.html', context)


@login_required(login_url='signin')
def delete_post(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        Post.objects.filter(id=post_id).delete()

        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
        user_posts = Post.objects.filter(user=user_object)
        user_number_of_posts = len(user_posts)

        user_number_of_followers = len(
            Followers.objects.filter(user=user_object))
        user_number_of_following = len(
            Followers.objects.filter(follower=user_object))

        context = {
            'user_object': user_object,
            'user_profile': user_profile,
            'user_posts': user_posts,
            'user_number_of_posts': user_number_of_posts,
            'user_number_of_followers': user_number_of_followers,
            'user_number_of_following': user_number_of_following,
        }

        return render(request, 'myposts.html', context)
    else:
        return myposts(request)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                # log user in and redirect to settigs page
                user_login = auth.authenticate(
                    username=username, password=password)
                auth.login(request, user_login)
                # create a Profie object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(
                    user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            # the user does not have an account and is trying to log in
            messages.info(request, 'Invalid Username or Password')
            return redirect('signin')
    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
