from django.contrib import admin
from .models import UserProfile,Post
# Register your models here.



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'first_name', 'last_name',)
    search_fields = ('user__username', 'email', 'first_name', 'last_name')
    list_filter = ('user__is_active',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'image','created_at')
    search_fields = ('id', 'user', 'text', 'created_at') 


admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Post,PostAdmin)
