from rest_framework import serializers
from .models import Blog

# v1: basic
class BlogSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content']

# v2: advanced
class BlogSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'category', 'tags', 'view_count']
