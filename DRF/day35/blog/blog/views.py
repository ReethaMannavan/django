from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Blog
from .serializers import BlogSerializerV1, BlogSerializerV2

class BlogView(APIView):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return BlogSerializerV2
        return BlogSerializerV1

    # GET all blogs or a single blog
    def get(self, request, pk=None):
        serializer_class = self.get_serializer_class()
        if pk:  # detail view
            try:
                blog = Blog.objects.get(pk=pk)
            except Blog.DoesNotExist:
                return Response({"detail": "Not found."}, status=404)
            serializer = serializer_class(blog)
        else:  # list view
            blogs = Blog.objects.all()
            serializer = serializer_class(blogs, many=True)
        return Response(serializer.data)

    # POST a new blog
    def post(self, request, pk=None):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()  # author optional
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

