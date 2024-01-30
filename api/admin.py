from django.contrib import admin
from .models import Account, Session, Subreddit, Subscription, Post, Comment, Vote, CommentVote


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'userId']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'userId']


@admin.register(Subreddit)
class SubredditAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'creator']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user__email', 'user__name', 'subreddit']
    list_filter = ['user', 'subreddit']

    def user__email(self, obj):
        return obj.user.email

    def user__name(self, obj):
        return obj.user.name


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'subreddit']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


@admin.register(CommentVote)
class CommentVoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'commentVoteType']
