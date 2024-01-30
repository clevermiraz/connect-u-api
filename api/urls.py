from django.urls import path
from .views import (CreateCommunity, SubRedditInfo, CheckSubscription,
                    RelatedSubredditPosts, CreatePost, SubscribedCommunities,
                    SubredditPosts, SubredditPostVotes)

urlpatterns = [
    path('create-community/', CreateCommunity.as_view(), name='create-community'),
    path('r/subreddit-info/<slug:name>/', SubRedditInfo.as_view(), name='subreddit-info'),

    path('r/check-subreddit-subscription/', CheckSubscription.as_view(), name='check-subscription'),
    path('r/toggle-subreddit-subscription/', CheckSubscription.as_view(), name='subscribe'),

    path('subreddit/posts/<slug:name>/', RelatedSubredditPosts.as_view(), name='related-subreddit-posts'),
    path('r/create-post/', CreatePost.as_view(), name='create-post'),
    path('r/posts/', SubredditPosts.as_view(), name='subreddit-posts'),

    path('subscriptions/', SubscribedCommunities.as_view(), name='subscriptions'),

    path('r/votes/post/', SubredditPostVotes.as_view(), name='post-votes'),
    path('r/votes/', SubredditPostVotes.as_view(), name='post-votes'),
]
