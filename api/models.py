from django.conf import settings
import uuid
from django.db import models


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    userId = models.CharField(max_length=255)
    accountType = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    providerAccountId = models.CharField(max_length=255)
    refreshToken = models.TextField(null=True)
    accessToken = models.TextField(null=True)
    expiresAt = models.IntegerField(null=True)
    tokenType = models.CharField(max_length=255, null=True)
    scope = models.CharField(max_length=255, null=True)
    idToken = models.TextField(null=True)
    sessionState = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.accountType


class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sessionToken = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    userId = models.CharField(max_length=255)
    expires = models.DateTimeField()

    def __str__(self):
        return self.sessionToken


class Subreddit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    userId = models.CharField(max_length=255)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    subredditId = models.CharField(max_length=255)

    def __str__(self):
        return self.subreddit.name


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    content = models.JSONField(null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    authorId = models.CharField(max_length=255)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    subredditId = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    text = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    authorId = models.CharField(max_length=255)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    postId = models.CharField(max_length=255)
    replyTo = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    commentId = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.text


class Vote(models.Model):
    VOTE_CHOICES = [
        ('UP', 'Up'),
        ('DOWN', 'Down'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    userId = models.CharField(max_length=255)
    post = models.ForeignKey(Post, related_name='votes', on_delete=models.CASCADE)
    postId = models.CharField(max_length=255)
    voteType = models.CharField(max_length=255, choices=VOTE_CHOICES)

    def __str__(self):
        return self.voteType


class CommentVote(models.Model):
    VOTE_CHOICES = [
        ('UP', 'Up'),
        ('DOWN', 'Down'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    userId = models.CharField(max_length=255)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    commentId = models.CharField(max_length=255)
    commentVoteType = models.CharField(max_length=255, choices=VOTE_CHOICES)

    def __str__(self):
        return self.commentVoteType
