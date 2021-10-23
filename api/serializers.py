from rest_framework import serializers
from network.models import Post, CustomUser, PostLikes


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    author_id = serializers.IntegerField(source='author.id')
    date_modified = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('id', 'author_id', 'author', 'title', 'text', 'created_date', 'date_modified', 'likes')


class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author_id = serializers.SerializerMethodField()
    date_modified = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('id', 'author_id', 'author', 'title', 'text', 'created_date', 'date_modified')

    def get_author_id(self, obj):
        return self.context['request'].user.id


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'date_joined', 'password')
