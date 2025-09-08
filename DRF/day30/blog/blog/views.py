from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import BlogPost, Comment
from .serializers import BlogPostSerializer, CommentSerializer

# -------------------------
# CBVs for BlogPost CRUD
# -------------------------
class BlogPostListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

# -------------------------
# FBV: Retrieve all comments for a blog post
# -------------------------
@api_view(['GET'])
def comments_for_post(request, post_id):
    try:
        post = BlogPost.objects.get(id=post_id)
    except BlogPost.DoesNotExist:
        return Response({"error": "Blog post not found"}, status=404)

    comments = post.comments.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

# -------------------------
# FBV: Create a comment for a blog post
# -------------------------
@api_view(['POST'])
def add_comment(request, post_id):
    try:
        post = BlogPost.objects.get(id=post_id)
    except BlogPost.DoesNotExist:
        return Response({"error": "Blog post not found"}, status=404)

    data = request.data.copy()
    data['blog_post'] = post.id  # link comment to this post
    serializer = CommentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
