from django.contrib import admin
from .models import UserProfile,Post,LikePost,Followers
# Register your models here.



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'first_name', 'last_name',)
    search_fields = ('user__username', 'email', 'first_name', 'last_name')
    list_filter = ('user__is_active',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'image','created_at','no_of_likes')
    search_fields = ('id', 'user', 'text', 'created_at','no_of_likes') 

class LikePostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'username')
    search_fields = ('post_id','username')  

class FollowersAdmin(admin.ModelAdmin):
    list_display = ('connection_id','follower','user')
    search_fields = ('connection_id','follower','user')       


admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(LikePost,LikePostAdmin)
admin.site.register(Followers,FollowersAdmin)