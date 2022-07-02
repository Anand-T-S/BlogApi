from django.urls import path
from BlogApi import views

urlpatterns = [
    path("blogs", views.BlogsView.as_view()),
    path("blogs/like/<int:blog_id>", views.BlogLikeView.as_view()),
    path("blogs/comments/<int:blog_id>", views.CommentsView.as_view()),

]