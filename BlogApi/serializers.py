from rest_framework.serializers import ModelSerializer
from BlogApi.models import Blogs, Comments
from django.contrib.auth.models import User
from rest_framework import serializers


class BlogSerializer(ModelSerializer):
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Blogs
        exclude = ("posted_date", "liked_by")

    def create(self, validated_data):
        user = self.context["user"]
        return Blogs.objects.create(**validated_data, author=user)


class CommentSerializer(ModelSerializer):
    user = serializers.CharField(read_only=True)
    blog = serializers.CharField(read_only=True)

    class Meta:
        model = Comments
        fields = ["blog", "comment", "user"]

    def create(self, validated_data):
        user = self.context.get("user")
        blog = self.context.get("blog")
        return Comments.objects.create(**validated_data, blog=blog, user=user)