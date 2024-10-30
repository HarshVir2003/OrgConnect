from Feeds.models import Posts, Likes, Comments
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from Feeds.Serializer import CommentsSerializers, LikesSerializers, PostsSerializer
from Feeds.processing import DataBuilder


class FeedView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostsSerializer
    http_method_names = ['get']

    def get_queryset(self):
        data = DataBuilder(self.request.user)
        return data.get_data()

    def get(self, request, *args, **kwargs):
        try:
            data = self.get_queryset()
            serializer = self.serializer_class(data, many=True)
            return Response(serializer.data)
        except Posts.DoesNotExist:
            return Response({'message': 'No Posts'}, status=status.HTTP_404_NOT_FOUND)


class PostsPostingView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostsSerializer
    http_method_names = ['post', 'put' 'delete']

    def post(self, request):
        serializer = PostsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    # def put(self, request):
    #     try:
    #         post = Posts.objects.get(user_id=request.user, id=request.data['id'])
    #     except Posts.DoesNotExist:
    #         return Response({'message': 'Achievement does not exists'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        try:
            post = Posts.objects.get(user_id=request.user, id=request.data['id'])
        except Posts.DoesNotExist:
            return Response({'message': 'Post does not exists'}, status=status.HTTP_404_NOT_FOUND)

        post.delete()
        return Response({'message': 'Post deleted'}, status=status.HTTP_200_OK)


class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentsSerializers
    http_method_names = ['post', ' get', 'delete']

    def get_queryset(self):
        post_id = self.kwargs.get('id')
        return Comments.objects.filter(post_id=post_id)

    def get(self, request):
        try:
            data = self.get_queryset()
            serializer = self.serializer_class(data, many=True)
            return Response(serializer.data)
        except Posts.DoesNotExists:
            return Response({'message': 'No Comments'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = CommentsSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        try:
            comment = Comments.objects.get(user_id=request.user, id=request.data['id'])
        except Comments.DoesNotExist:
            return Response({'message': 'comment doesnot exist'}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response({'message': 'comment deleted successfully'}, status=status.HTTP_200_OK)


class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentsSerializers
    http_method_names = ['post', 'delete']

    def post(self, request):
        serializer = LikesSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        try:
            like = Likes.objects.get(user_id=request.user, id=request.data['id'])
        except Likes.DoesNotExist:
            return Response({'message': 'like doesnot exist'}, status=status.HTTP_404_NOT_FOUND)

        like.delete()
        return Response({'message': 'disliked'}, status=status.HTTP_200_OK)
