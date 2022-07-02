from django.shortcuts import render
from rest_framework.views import APIView
from BlogApi.serializers import BlogSerializer, CommentSerializer
from rest_framework.response import Response
from BlogApi.models import Blogs, Comments
from rest_framework import permissions, authentication

# Create your views here.


class BlogsView(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]

    def get(self, request, *args, **kwargs):
        qs = Blogs.objects.all()
        serializer = BlogSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = BlogSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class BlogLikeView(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        blog_id = kwargs.get("blog_id")
        blog = Blogs.objects.get(id=blog_id)
        blog.liked_by.add(request.user)
        total_likes = blog.liked_by.all().count()
        return Response({"liked_count":total_likes})


class CommentsView(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args,**kwargs):
        blog_id = kwargs.get("blog_id")
        comments = Comments.object.filter(blog=blog_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        blog_id = kwargs.get("blog_id")
        blog = Blogs.objects.get(id=blog_id)
        serializer = CommentSerializer(data=request.data, context={"blog": blog, "user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
