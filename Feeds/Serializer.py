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

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user
        return super().create(validated_data)


class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user
        return super().create(validated_data)


class LikesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user
        return super().create(validated_data)
