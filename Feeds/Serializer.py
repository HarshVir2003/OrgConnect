from rest_framework import serializers
from Feeds.models import Posts, Comments, Likes



class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'


class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class LikesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'


