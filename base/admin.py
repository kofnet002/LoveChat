from django.contrib import admin
from .models import Follow, User, Post, LikePost, Comment
from chat.models import ChatMessage


@admin.register(User)
class UserModel(admin.ModelAdmin):
    list_display = ('username',)


admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(ChatMessage)
