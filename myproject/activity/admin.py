from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserActivityLog

@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'status', 'timestamp')
    list_filter = ('action', 'status', 'timestamp')
    search_fields = ('user__username', 'action', 'metadata')
