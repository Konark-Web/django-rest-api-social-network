import jwt
import datetime
from django.contrib.auth import user_logged_in
from django.shortcuts import get_object_or_404
from django.utils import timezone

from django.db.models import Count
from django.db.models.functions import TruncDay

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler

from . import serializers
from network.models import Post, CustomUser, PostLikes
from social import settings


class PostList(APIView):
    def get(self):
        post_obj = Post.objects.all()
        serializer = serializers.PostSerializer(post_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostDetail(APIView):
    def get(self, request, pk):
        post_obj = get_object_or_404(Post, pk=pk)
        serializer = serializers.PostSerializer(post_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = serializers.PostCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostLike(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        user = self.request.user
        response = {}

        if post:
            response['message'] = 'You successfully liked the post'

            like = PostLikes.objects.filter(post_id=post, user_id=user).first()
            if like:
                if like.type == 1:
                    like.type = 0
                    post.likes = post.likes - 1
                    response['message'] = 'You successfully unliked the post'
                elif like.type == 0:
                    like.type = 1
                    post.likes = post.likes + 1

                like.date = timezone.now()
            else:
                like = PostLikes(post_id=post, user_id=user, type=1)
                post.likes = post.likes + 1

            post.save()
            like.save()

            return Response(response, status=status.HTTP_200_OK)
        else:
            response['message'] = f'Post with ID {pk} not found'
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class PostLikeAnalytics(APIView):
    def get(self, request):
        response = {}
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')

        if date_from:
            try:
                date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')

                if date_to:
                    date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')
                else:
                    date_to = datetime.datetime.now()
            except ValueError:
                response['message'] = 'You entered an incorrect date format.'
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            likes_obj = PostLikes.objects\
                .annotate(day=TruncDay('date'))\
                .values('day')\
                .annotate(c=Count('id'))\
                .values('day', 'c')\
                .filter(type=1, date__range=(date_from, date_to))

            if likes_obj:
                for like in likes_obj:
                    date = like['day'].strftime('%Y-%m-%d')
                    response[date] = like['c']

                return Response(response, status=status.HTTP_200_OK)

        response['message'] = 'No likes for this period.'
        return Response(response, status=status.HTTP_404_NOT_FOUND)


class CreateUser(APIView):
    def post(self, request):
        user = request.data

        serializer = serializers.UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AuthenticateUser(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = CustomUser.objects.get(email=email, password=password)
        if user:
            payload = jwt_payload_handler(user)
            token = jwt.encode(payload, settings.SECRET_KEY)
            user_details = {'name': "%s %s" % (
                user.first_name, user.last_name), 'token': token}
            user_logged_in.send(sender=user.__class__,
                                request=request, user=user)
            return Response(user_details, status=status.HTTP_200_OK)


