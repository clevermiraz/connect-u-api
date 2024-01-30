from datetime import datetime

from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CustomUserSerializer


class RegisterUserView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        full_name = data.get('name')
        email = data.get('email')
        image = data.get('image')
        provider = data.get('provider')
        providerAccountId = data.get('providerAccountId')

        CustomUser = get_user_model()
        try:
            # check if user already exists
            user = CustomUser.objects.get(email=email)

            # if user exists, and not have username then update the username
            if not user.username:
                user.username = username
                user.save()
                return Response('Username Added Successfully', status=status.HTTP_200_OK)

            serializer = CustomUserSerializer(user, many=False)

            # if user exists, return user
            return Response(serializer.data, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(
                username=username,
                name=full_name,
                email=email,
                image=image,
                emailVerified=datetime.now(tz=timezone.utc),
                provider=provider,
                providerAccountId=providerAccountId
            )

            serializer = CustomUserSerializer(user, many=False)

            # if user does not exist, create user
            return Response({'message': 'User Created Successfully', 'user': serializer.data}, status=status.HTTP_201_CREATED)
