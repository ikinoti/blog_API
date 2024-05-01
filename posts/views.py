

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view, APIView, permission_classes

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

    def get(self, request:Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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

    def get(self, request:Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request:Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

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

    def get(self, request:Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)