from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from BlogApi.models import Blogs
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            # "first_name",
            # "last_name",
            "username",
            "email",
            "password"
        ]


class PostSerializer(ModelSerializer):
    author = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)
    # liked_by = serializers.CharField(read_only=True)

    class Meta:
        model = Blogs
        exclude = ("posted_date",)
        depth = 1

    def create(self, validated_data):
        user = self.context.get("user")
        return Blogs.objects.create(**validated_data, author=user)
