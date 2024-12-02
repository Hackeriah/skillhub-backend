from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['firstname','is_active', 'email']
    list_editable=['is_active']


admin.site.register(User,UserAdmin)