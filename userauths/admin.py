from django.contrib import admin
from userauths.models import User, Profile
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'custom_active_status']
    exclude = ['password', 'date_joined', 'groups', 'staff_status', 'first_name', 'last_name', 'last_login', 'is_superuser', 'user_permissions', 'is_staff']
    readonly_fields = ['email', 'username']
    def custom_active_status(self, obj):
        return obj.is_active  # This is the field you want to rename

    custom_active_status.boolean = True
    custom_active_status.short_description = 'Ban/Inactive'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'bio', 'phone']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)