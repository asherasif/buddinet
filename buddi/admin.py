from django.contrib import admin
from .models import UserProfile
# Register your models here.



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'first_name', 'last_name',)
    search_fields = ('user__username', 'email', 'first_name', 'last_name')
    list_filter = ('user__is_active',)


admin.site.register(UserProfile,UserProfileAdmin)
