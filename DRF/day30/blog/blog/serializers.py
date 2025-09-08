from rest_framework import serializers
from .models import BlogPost, Comment

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'

    # Validate unique title (extra validation)
    def validate_title(self, value):
        if BlogPost.objects.filter(title=value).exists():
            raise serializers.ValidationError("Blog post title must be unique.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    # Validate that comment_text is not empty
    def validate_comment_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment text cannot be empty.")
        return value
