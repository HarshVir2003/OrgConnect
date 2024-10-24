from rest_framework import serializers
from Feeds.models import Posts, Comments, Likes


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ...


class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ...


class LikesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ...
