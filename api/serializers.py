from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import Subreddit, Post, Vote, Comment, Subscription


class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'voteType', 'user', 'userId', 'post', 'postId']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'createdAt', 'author', 'authorId', 'post', 'postId', 'replyTo', 'commentId']


class PostSerializer(ModelSerializer):
    votes = VoteSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    subredditName = StringRelatedField(source='subreddit.name')
    authorUsername = StringRelatedField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'createdAt', 'updatedAt', 'author', 'authorUsername',
                  'authorId', 'subreddit', 'subredditName', 'subredditId', 'votes', 'comments']
        # depth = 1


class SubredditSerializer(ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Subreddit
        fields = ['id', 'name', 'creator', 'createdAt', 'posts']


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'userId', 'subreddit', 'subredditId']
