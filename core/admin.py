from django.contrib import admin
from .models import CustomUser, Comment, Blog, Vote

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','email','phone_number','profile_picture']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=['title','picture','description','is_deleted','created_by','updated_by']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['content','blog','is_deleted','created_by','updated_by']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display=['value','blog','user']