from drf_yasg.utils import swagger_auto_schema

from Feeds.models import Posts, Likes, Comments
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from Feeds.Serializer import CommentsSerializers, LikesSerializers, PostsSerializer
from Feeds.processing import DataBuilder
from Feeds.pagination import CustomPagination
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser


page_param = openapi.Parameter(
    'page',
    openapi.IN_QUERY,
    description="Page number for pagination. Defaults to 1.",
    type=openapi.TYPE_INTEGER,
    required=False,
    default=1
)


class FeedView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostsSerializer
    http_method_names = ['get']

    def get_queryset(self):
        data = DataBuilder(self.request.user)
        return data.get_data()

    @swagger_auto_schema(
        operation_summary="Retrieve paginated posts visible to the user.",
        operation_description=(
                "Use this endpoint to get a list of posts the authenticated user is allowed to view. "
                "Supports pagination using the `page` query parameter. Example: "
                "[http://localhost:8000/feeds/?page=1](http://localhost:8000/feeds/?page=1)"
        ),
        manual_parameters=[page_param])
    def get(self, request, *args, **kwargs):
        try:
            data = self.get_queryset()
            paginator = CustomPagination()
            data = paginator.paginate_queryset(data, request, view=self)
            serializer = self.serializer_class(data, many=True)
            return Response(serializer.data)
        except Posts.DoesNotExist:
            return Response({'message': 'No Posts'}, status=status.HTTP_404_NOT_FOUND)


class PostsPostingView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostsSerializer
    http_method_names = ['post', 'delete']
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Post the User's post's here",
        operation_description='post the valid data.',
        request_body=PostsSerializer

    )
    def post(self, request):
        # Add user_id directly to request data
        data = request.data.copy()
        data['user_id'] = request.user.id

        # Initialize the serializer with the modified data
        serializer = self.serializer_class(data=data, context={'request': request})

        # Validate the serializer and save if valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Return errors if validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a post",
        operation_description="Deletes a post if it belongs to the authenticated user. Requires the post ID to be provided in the URL.", )
    def delete(self, request, id=None):
        if not id:
            return Response({'message': 'id missing'}, status=status.HTTP_404_NOT_FOUND)
        try:
            post = Posts.objects.get(user_id=request.user, id=id)
        except Posts.DoesNotExist:
            return Response({'message': 'Post Not yours'}, status=status.HTTP_404_NOT_FOUND)

        post.delete()
        return Response({'message': 'Post deleted'}, status=status.HTTP_200_OK)


class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentsSerializers
    http_method_names = ['post', 'get', 'delete']

    def get_queryset(self, post_id):
        return Comments.objects.filter(post_id=post_id)

    @swagger_auto_schema(operation_summary='Get comments of a post.',
                         operation_description='pass in post id to get comments for the post')
    def get(self, request, id=None):
        try:
            data = self.get_queryset(id)
            serializer = self.serializer_class(data, many=True)
            return Response(serializer.data)
        except Posts.DoesNotExists:
            return Response({'message': 'No Comments'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(operation_summary='Create a comment on a post.',
                         operation_description='here we can create a post comment pass in required data',
                         request_body=CommentsSerializers)
    def post(self, request):
        d = {}
        for x in request.data:
            d[x] = request.data[x]
        d['user_id'] = request.user.id
        serializer = self.serializer_class(data=d, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(operation_summary='delete a comment', operation_description='pass in comment id to delete the comment')
    def delete(self, request, id=None):
        if not id:
            return Response({'message': 'no comment'}, status=status.HTTP_404_NOT_FOUND)
        try:
            comment = Comments.objects.get(user_id=request.user.id, id=id)
        except Comments.DoesNotExist:
            return Response({'message': 'comment doesnot exist'}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response({'message': 'comment deleted successfully'}, status=status.HTTP_200_OK)


class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikesSerializers
    http_method_names = ['post', 'delete']
    @swagger_auto_schema(operation_summary='Like a post',operation_description='pass in the data to like a post', request_body=LikesSerializers)
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
    @swagger_auto_schema(operation_summary='dislike a post', operation_description='pass in the post id to dislike')
    def delete(self, request, id=None):
        if not id:
            return Response({'message': 'id missing'}, status=status.HTTP_404_NOT_FOUND)
        try:
            post = Posts.objects.get(id=id)
            like = Likes.objects.get(user_id=request.user, post_id=post.id)
        except Likes.DoesNotExist:
            return Response({'message': 'like doesnot exist'}, status=status.HTTP_404_NOT_FOUND)

        like.delete()
        return Response({'message': 'disliked'}, status=status.HTTP_200_OK)
