from rest_framework import serializers
from Feeds.models import Posts, Comments, Likes


class PostsSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = '__all__'

    def get_like_count(self, obj):
        return Likes.objects.filter(post_id=obj.id).count()

    def get_comment_count(self, obj):
        return Comments.objects.filter(post_id=obj.id).count()


class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class LikesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'
