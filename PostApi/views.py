from django.shortcuts import render
from django.contrib.auth.models import User
from PostApi.serializers import PostSerializer, UserSerializer
from BlogApi.models import Blogs
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import action

# Create your views here.
# http://127.0.0.1:8000/api/v3/posts/
# http://127.0.0.1:8000/api/v3/posts/


# class UserCreationView(ModelViewSet):
#     model = User
#     serializer_class = UserSerializer


class PostViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    model = Blogs
    serializer_class = PostSerializer
    queryset = Blogs.objects.all()

    def get_object(self, id):
        return Blogs.objects.get(id=id)

    def get_queryset(self):
        return Blogs.objects.filter(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @action(["GET"], detail=True)
    def get_likes(self, request, *args, **kwargs):
        post = self.get_object()
        print(post)
        data = post.liked_by.all()
        print(data)
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data)

    @action(["GET"], detail=True)
    def add_like(self, request, *args, **kwargs):
        user = self.request.user
        post = self.get_object(kwargs.get("pk"))
        post.liked_by.add(user)
        post.save()
        return Response({"msg":"ok"})

    @action(["GET"], detail=False)
    def all_post(self, request, *args, **kwargs):
        qs = Blogs.objects.all()
        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        blog = Blogs.objects.get(id=id)
        serializer = PostSerializer(blog)
        return Response(serializer.data)
