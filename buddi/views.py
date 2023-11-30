from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import UserProfile,Post,LikePost,Followers
from django.contrib.auth.decorators import login_required
from itertools import chain
# Create your views here.


@login_required(login_url='login')
def newsfeed(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user_object)

    # Fetch users the current user is following
    user_follow_list = Followers.objects.filter(follower=request.user.username).values_list('user', flat=True)

     # Include the current user in the list
    user_follow_list = list(user_follow_list)
    user_follow_list.append(request.user.username)

    # Fetch posts from the users the current user is following
    feed_lists = Post.objects.filter(user__username__in=user_follow_list)

    # Order the posts by timestamp or any other criteria you desire
    feed_lists = feed_lists.order_by('created_at')

    return render(request, 'newsfeed.html', {'user_profile': user_profile, 'posts': feed_lists})


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
        return redirect('/')


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

@login_required(login_url='login')
def profile(request, pk):

    user_object= User.objects.get(username=pk)
    user_profile = UserProfile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=user_object)
    user_post_len = len(user_posts)


    follower = request.user.username
    user_to_follow = pk

    if Followers.objects.filter(follower = follower, user = user_to_follow).first():
        btn_text = "Unfollow"
    else:
        btn_text = "Follow" 

    follower_count = len(Followers.objects.filter(user = pk))       
    following_count = len(Followers.objects.filter(follower = pk))       

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_len' : user_post_len,
        'btn_text' : btn_text,
        'follower_count':follower_count,
        'following_count': following_count
    }

    return render(request,'profile.html',context)

@login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        follower = request.user.username
        user_to_follow = request.POST['user_to_follow']

        if Followers.objects.filter(follower = follower, user = user_to_follow).exists():
            delete_follow = Followers.objects.get(follower = follower, user = user_to_follow)
            delete_follow.delete()
        else:
            new_follow = Followers.objects.create(follower = follower, user = user_to_follow)
            new_follow.save()

        return redirect('/profile/'+user_to_follow)
    else:
        return redirect('/profile/'+user_to_follow)
    