from django.contrib import admin
from core.models import Post, Gallery, FriendRequest, Notification, Comment, Friend, ReplyComment, ChatMessage



class FriendRequestAdmin(admin.ModelAdmin):
    list_editable = ['status']
    list_display = ['sender', 'receiver', 'status']

class FriendAdmin(admin.ModelAdmin):
    list_display = ['user', 'friend']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'sender', 'post', 'comment', 'is_read']

class GalleryAdmin(admin.TabularInline):
    model = Gallery

class CommentTabAdmin(admin.TabularInline):
    model = Comment

class ReplyCommentTabAdmin(admin.TabularInline):
    model = ReplyComment


class PostAdmin(admin.ModelAdmin):
    inlines = [GalleryAdmin, CommentTabAdmin]
    list_editable = ['user', 'title', 'visibility']
    list_display = ['thumbnail', 'user', 'title', 'visibility']
    prepopulated_fields = {"slug": ("title", )}

class GroupAdmin(admin.ModelAdmin):
    # inlines = [GroupPostTabAdmin]
    list_editable = ['user', 'name', 'visibility']
    list_display = ['thumbnail', 'user', 'name', 'visibility']
    prepopulated_fields = {"slug": ("name", )}


class CommentAdmin(admin.ModelAdmin):
    inlines = [ReplyCommentTabAdmin]
    list_display = ['user', 'post', 'comment', 'active']


class ReplyAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'active']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'comment', 'active']


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'sender', 'reciever' ,'message','date', 'is_read']
    

    

admin.site.register(Notification, NotificationAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ReplyComment, ReplyAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)


