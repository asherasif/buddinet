from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import UserProfile,Post,LikePost,Followers,comments
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
# Create your views here.


@login_required(login_url='login')
def newsfeed(request):
    user_object = request.user
    user_profile = UserProfile.objects.get(user=user_object)

    # Fetch user IDs of users the current user is following
    following_user_ids = Followers.objects.filter(follower=user_object).values_list('followed_id', flat=True)

    # Include the current user's ID in the list
    user_ids = list(following_user_ids) + [user_object.id]

    # Fetch posts from the users the current user is following, including their own
    feed_lists = Post.objects.filter(user_id__in=user_ids).prefetch_related('comments1').order_by('-created_at')

    # User Suggestions Logic
    all_possible_users = User.objects.exclude(id=user_object.id)
    followed_users = User.objects.filter(id__in=user_ids)
    suggestions = all_possible_users.difference(followed_users)
    
    # Randomize user suggestions
    final_suggestions = list(suggestions)
    random.shuffle(final_suggestions)

    # Fetch user profiles for suggestions
    username_profile_list = UserProfile.objects.filter(user__in=final_suggestions[:3])

    # Comments on Post
    user_posts = Post.objects.filter(user=user_object)
    comments_list = comments.objects.filter(post__in=user_posts).order_by('post__created_at')

    return render(request, 'newsfeed.html', {
        'user_profile': user_profile, 
        'posts': feed_lists,
        'suggestions_list': username_profile_list,
        'comments_list': comments_list
    })


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')



def index(request):
    return render(request,'login.html')



def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        profile_img = request.FILES.get('profile_img')
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username Exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)

                user_profile = UserProfile.objects.create(user=user, email=email, first_name=first_name, last_name=last_name,profile_img=profile_img)

                return redirect('login')
        else:
            messages.info(request,"Password Not Matching")
            return redirect('signup')

    return render(request,'signup.html')

def login(request):


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('newsfeed')
        else:
            messages.info(request,'Incorrect Login/Password')
            return render(request,'login.html')
        
    else:
     return render(request,'login.html')
    
'''
@login_required(login_url='login')
def upload(request):

    if(request.method == 'POST'):
       user = request.user.username
       image = request.FILES.get('image')
       text = request.POST['text']

       new_post = Post.objects.create(user=user,image=image,text=text)
       new_post.save()

       return redirect('newsfeed')

    else:
        return redirect('/')

'''
@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        text = request.POST['text']

        # [Posts --> user] requires the whole User instance (ie the curreently logged in user ka instance and not just the ID)
        # ab ye [user=request.user] directly apko currently logged in walay ka instance poora dedeta hai, Django khud usmein se ID nikalta hai
        new_post = Post.objects.create(user=request.user, image=image, text=text)
        # No need to call save() as create() already saves the object
        return redirect('newsfeed')

    else:
        return redirect('newsfeed')


@login_required(login_url='login')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)
    like_check = LikePost.objects.filter(post_id=post_id,username=username).first()

    if like_check == None:
       new_like = LikePost.objects.create(post_id = post_id, username=username)
       new_like.save()
       post.no_of_likes = post.no_of_likes+1
       post.save()
       return redirect('newsfeed')
    else:
      like_check.delete()
      post.no_of_likes = post.no_of_likes-1
      post.save()
      return redirect('newsfeed')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .models import UserProfile, Post, Followers

User = get_user_model()

@login_required(login_url='login')
def profile(request, pk):
    user_object = get_object_or_404(User, username=pk)
    user_profile = UserProfile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=user_object)
    user_post_len = len(user_posts)

    # Check if the current user is following the profile user
    if Followers.objects.filter(follower=request.user, followed=user_object).exists():
        btn_text = "Unfollow"
    else:
        btn_text = "Follow"

    # Count the number of followers and followings
    follower_count = Followers.objects.filter(followed=user_object).count()
    following_count = Followers.objects.filter(follower=user_object).count()

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_len': user_post_len,
        'btn_text': btn_text,
        'follower_count': follower_count,
        'following_count': following_count
    }

    return render(request, 'profile.html', context)

 

def follow(request):
    if request.method == 'POST':
        follower = request.user  # The current logged-in user
        username_to_follow = request.POST.get('user_to_follow')  # Username of the user to follow/unfollow

        # Get the User object for the user to follow
        user_to_follow = get_object_or_404(User, username=username_to_follow)

        # Check if the follow relationship already exists
        existing_follow = Followers.objects.filter(follower=follower, followed=user_to_follow)
        if existing_follow.exists():
            # Unfollow logic: If they already follow, unfollow (delete the relationship)
            existing_follow.delete()
        else:
            # Follow logic: Create a new follow relationship
            Followers.objects.create(follower=follower, followed=user_to_follow)

        return redirect('/profile/' + username_to_follow)
    else:
        return redirect('/profile/' + request.POST.get('user_to_follow', ''))




'''
@login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        follower = request.user
        user_to_follow = request.POST['user_to_follow']

        if Followers.objects.filter(follower = follower, user = user_to_follow).exists():
            delete_follow = Followers.objects.get(follower = follower, followed = user_to_follow)
            delete_follow.delete()
        else:
            new_follow = Followers.objects.create(follower = follower, followed = user_to_follow)
            new_follow.save()

        return redirect('/profile/'+user_to_follow)
    else:
        return redirect('/profile/'+user_to_follow)
'''        



@login_required(login_url='login')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user = user_object)

    if request.method == 'POST':
       username = request.POST['username']
       username_obj = User.objects.filter(username__icontains=username)
       
       username_profile = []
       username_profile_list = []      

       for usernames in username_obj:
           username_profile.append(usernames.id)

       for idd in username_profile:
        profiles = UserProfile.objects.filter(user__id = idd)
        username_profile_list.append(profiles)

       username_profile_list = list(chain(*username_profile_list))     

    return render(request,'search.html',{'user_profile': user_profile,'username_profile_list': username_profile_list})


@login_required(login_url='login')
def comments_post(request):
    if request.method == 'POST':
        user = request.user
        text = request.POST.get('text')
        post_id = request.POST.get('post_id', '')  

       
        if post_id:
            try:
                post = Post.objects.get(id=post_id)
                new_comment = comments.objects.create(post=post, user=user, text=text)
                new_comment.save()
                
                comments_list = comments.objects.filter(post=post)
                return render(request, 'comments.html', {'post':post,'comments_list': comments_list})

            except Post.DoesNotExist:
                
                messages.error(request, 'Post does not exist.')
                return redirect('newsfeed')

