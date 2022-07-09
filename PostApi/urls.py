from django.urls import path
from PostApi import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("posts", views.PostViewSet, basename="post")
urlpatterns = []+router.urls
