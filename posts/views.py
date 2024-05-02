

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema

from .models import Post
from .serializers import PostSerializer
from accounts.serializers import CurrentUserPostsSerializer
from .permissions import ReadOnly, AuthorOrReadOnly

from django.shortcuts import get_object_or_404




@api_view(http_method_names=["GET", "POST"])
@permission_classes([AllowAny])
def homepage(request:Request):

    if request.method == "POST":
        data = request.data
        response={"message":"Hello World", "data":data}
        return Response(data=response, status=status.HTTP_201_CREATED)
     
    response={"message":"Hello World"}
    return Response(data=response, status=status.HTTP_200_OK)


class PostListCreateView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):

    """
        a view for creating and listing posts
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)

    @swagger_auto_schema(
            operation_summary="List all Posts",
            operation_description="This endpoint creates a post"
    )
    def get(self, request:Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
            operation_summary="Creates a Posts",
            operation_description="This returns a list of all posts"
    )
    def post(self, request:Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostRetrieveUpdateDeleteView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
    ):

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [AuthorOrReadOnly]

    @swagger_auto_schema(
            operation_summary="Retrieve a post by id",
            operation_description="This retrieves a post by an id"
    )
    def get(self, request:Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
            operation_summary="Updates a post by id",
            operation_description="This updates a post given the id"
    )
    def put(self, request:Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
            operation_summary="Deletes a post",
            operation_description="This deletes a post given the id"
    )
    def delete(self, request:Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def get_posts_for_current_user(request:Request):
    user = request.user

    serializer = CurrentUserPostsSerializer(
        instance=user,
        context = {"request":request}
        )

    return Response(
        data= serializer.data,
        status=status.HTTP_200_OK
    )

class ListPostsForAuthor(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # user = self.request.user
        # return Post.objects.filter(author=user)

        # username = self.kwargs.get("username")
        # return Post.objects.filter(author__username=username)

        username = self.request.query_params.get("username") or None
        queryset = Post.objects.all()

        if username is not None:
            return Post.objects.filter(author__username=username)
        
        return queryset

    @swagger_auto_schema(
            operation_summary="LIst posts for an author (user)",
            operation_description="This retrieves all post done by login user"
    )
    def get(self, request:Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)