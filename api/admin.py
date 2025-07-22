from django.contrib import admin

from api.models.models import *
from rest_framework_api_key.admin import APIKeyModelAdmin

class ScoresAdmin(admin.ModelAdmin):
    list_filter = ("created_at",)
    search_fields = ("name", "source_ipv4", "user_agent", "device", "ja4", "ja3")
    list_display = ["created_at","device", "source_ipv4","user_agent","reason", "is_safe", "score", "current_score_enhanced", "ja4", "ja4h", "ja4l", "ja3"]
admin.site.register(Scores,ScoresAdmin )

class UserAdmin(admin.ModelAdmin):
    list_filter = ("created_at",)
    search_fields = ("email",)
    list_display = ["created_at","email", "active"]
admin.site.register(User, UserAdmin)

class DevicesAdmin(admin.ModelAdmin):
    list_filter = ("created_at",)
    search_fields = ("user", "prefix")
    list_display = ["created_at","name","User", "verified"]
admin.site.register(Devices,DevicesAdmin)