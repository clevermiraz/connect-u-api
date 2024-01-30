from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Subreddit, Subscription, Post, Vote
from .serializers import SubredditSerializer, PostSerializer, SubscriptionSerializer, VoteSerializer


class CreateCommunity(APIView):
    def post(self, request):
        data = request.data
        name = data.get('name')
        creatorId = data.get('id')

        if not name or not creatorId:
            return Response({'message': 'SubReddit Name is required'}, status=status.HTTP_400_BAD_REQUEST)

        # check is Subreddit Exists.
        try:
            sub_reddit = Subreddit.objects.get(name=name)

            if sub_reddit:
                return Response({'message': 'SubReddit Already Exists'}, status=status.HTTP_409_CONFLICT)

        except Subreddit.DoesNotExist:
            CustomUser = get_user_model()
            creator = CustomUser.objects.get(id=creatorId)
            sub_reddit = Subreddit.objects.create(name=name, creator=creator)

            # creator Also has to be subscribed to the subreddit.
            Subscription.objects.create(user=creator,
                                        userId=creator.id,
                                        subredditId=sub_reddit.id,
                                        subreddit=sub_reddit)

            serializer = SubredditSerializer(sub_reddit, many=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubscribedCommunities(APIView):
    def get(self, request):
        data = request.GET
        userId = data.get('userId')

        if not userId:
            return Response({'message': 'User Id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_model().objects.get(id=userId)
            subscriptions = Subscription.objects.filter(user=user)

            serializer = SubscriptionSerializer(subscriptions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except get_user_model().DoesNotExist:
            return Response({'message': 'User Does Not Exist'}, status=status.HTTP_204_NO_CONTENT)


class SubRedditInfo(APIView):
    def get(self, request, name):
        try:
            sub_reddit = Subreddit.objects.get(name=name)

            # check memberCount of the subreddit.
            memberCount = Subscription.objects.filter(subreddit=sub_reddit).count()

            serializer = SubredditSerializer(sub_reddit, many=False)
            return Response({'subreddit': serializer.data, 'memberCount': memberCount}, status=status.HTTP_200_OK)

        except Subreddit.DoesNotExist:
            return Response({'message': 'SubReddit Does Not Exist'}, status=status.HTTP_204_NO_CONTENT)


class CheckSubscription(APIView):
    def get(self, request):
        data = request.GET
        subredditId = data.get('subredditId')
        userId = data.get('userId')

        if not subredditId or not userId:
            return Response({'message': 'SubReddit Id and User Id are required', 'status': False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sub_reddit = Subreddit.objects.get(id=subredditId)
            user = get_user_model().objects.get(id=userId)

            try:
                Subscription.objects.get(subreddit=sub_reddit, user=user)
                return Response({'message': 'Subscribed', 'status': True}, status=status.HTTP_200_OK)

            except Subscription.DoesNotExist:
                return Response({'message': 'Not Subscribed', 'status': False}, status=status.HTTP_204_NO_CONTENT)

        except Subreddit.DoesNotExist:
            return Response({'message': 'SubReddit Does Not Exist', 'status': False}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        # toggle subscription (subscribe/unsubscribe)
        data = request.data
        subredditId = data.get('subredditId')
        userId = data.get('userId')

        if not subredditId or not userId:
            return Response({'message': 'SubReddit Id and User Id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sub_reddit = Subreddit.objects.get(id=subredditId)
            user = get_user_model().objects.get(id=userId)

            try:
                # check if user is the owner of the subreddit
                if sub_reddit.creator == user:
                    return Response(
                        {'message': 'You are the owner of the subreddit, so you can not unsubscribe from your own subreddit'},
                        status=status.HTTP_403_FORBIDDEN
                    )

                subscription = Subscription.objects.get(subreddit=sub_reddit, user=user)
                subscription.delete()
                return Response({'message': 'Unsubscribed'}, status=status.HTTP_200_OK)

            except Subscription.DoesNotExist:
                Subscription.objects.create(subreddit=sub_reddit, user=user)
                return Response({'message': 'Subscribed'}, status=status.HTTP_201_CREATED)

        except Subreddit.DoesNotExist:
            return Response({'message': 'SubReddit Does Not Exist'}, status=status.HTTP_204_NO_CONTENT)


# related subreddit posts
class RelatedSubredditPosts(APIView):
    def get(self, request, name):
        try:
            sub_reddit = Subreddit.objects.get(name=name)

            serializer = SubredditSerializer(sub_reddit)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Subreddit.DoesNotExist:
            return Response({'message': 'SubReddit Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)


class CreatePost(APIView):
    def post(self, request):
        data = request.data
        title = data.get('title')
        content = data.get('content')
        authorId = data.get('authorId')
        subredditId = data.get('subredditId')

        if not title or not content or not authorId or not subredditId:
            return Response({'message': 'Title, Content, Author Id and SubReddit Id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            author = get_user_model().objects.get(id=authorId)
            subreddit = Subreddit.objects.get(id=subredditId)

            post = Post.objects.create(title=title,
                                       content=content,
                                       author=author,
                                       authorId=author.id,
                                       subreddit=subreddit,
                                       subredditId=subreddit.id)

            serializer = PostSerializer(post, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except get_user_model().DoesNotExist:
            return Response({'message': 'Author Does Not Exist'}, status=status.HTTP_204_NO_CONTENT)

        except Subreddit.DoesNotExist:
            return Response({'message': 'SubReddit Does Not Exist'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubredditPosts(APIView):
    def get(self, request):
        data = request.GET
        limit = data.get('limit')
        page = data.get('page')
        subredditName = data.get('subredditName')

        if not limit or not page or not subredditName:
            return Response({'message': 'Limit, Page and SubReddit Name are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subreddit = Subreddit.objects.get(name=subredditName)

            posts = Post.objects.select_related('subreddit', 'author').prefetch_related('votes', 'comments')
            posts = posts.filter(subreddit=subreddit).order_by('-createdAt')[((int(page) - 1) * int(limit)):(int(page) * int(limit))]

            serializer = PostSerializer(posts, many=True)

            # Calculate total number of pages
            # total_pages = (posts.count() + int(limit) - 1) // int(limit)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Subreddit.DoesNotExist:
            return Response({'message': 'SubReddit Does Not Exist'}, status=status.HTTP_204_NO_CONTENT)


class SubredditPostVotes(APIView):
    def get(self, request):
        try:
            data = request.GET
            postId = data.get('postId')
            userId = data.get('userId')

            if not postId or not userId:
                return Response({'message': 'Post Id and User Id are required'}, status=status.HTTP_400_BAD_REQUEST)

            post = Post.objects.get(id=postId)
            user = get_user_model().objects.get(id=userId)

            try:
                vote = post.votes.get(user=user)
                serializer = VoteSerializer(vote, many=False)

                return Response(serializer.data, status=status.HTTP_200_OK)

            except post.votes.model.DoesNotExist:
                return Response({'message': 'Not Voted'}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist:
            return Response({'message': 'Post Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = request.data
        userId = data.get('userId')
        postId = data.get('postId')
        voteType = data.get('voteType')

        if not userId or not postId or not voteType:
            return Response({'message': 'User Id, Post Id and Vote Type are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(id=postId)
            user = get_user_model().objects.get(id=userId)

            try:
                vote = post.votes.get(user=user)
                vote.voteType = voteType
                vote.save()

                serializer = VoteSerializer(vote, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except post.votes.model.DoesNotExist:
                vote = post.votes.create(user=user, userId=user.id, voteType=voteType, postId=postId)

                serializer = VoteSerializer(vote, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Post.DoesNotExist:
            return Response({'message': 'Post Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        data = request.data
        userId = data.get('userId')
        existingVoteId = data.get('existingVoteId')
        voteType = data.get('voteType')

        if not existingVoteId or not voteType:
            return Response({'message': 'Existing Vote Id and Vote Type are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vote = Vote.objects.get(id=existingVoteId)
            # check if the user is the owner of the vote
            if vote.userId != userId:
                return Response({'message': 'You are not the owner of the vote'}, status=status.HTTP_403_FORBIDDEN)

            if vote.userId == userId and vote.voteType == voteType:
                # delete the vote
                vote.delete()
                return Response({'message': 'Vote Deleted'}, status=status.HTTP_200_OK)

            else:
                vote.voteType = voteType
                vote.save()

                serializer = VoteSerializer(vote)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Vote.DoesNotExist:
            return Response({'message': 'Vote Does Not Exist'}, status=status.HTTP_204_NO_CONTENT)
