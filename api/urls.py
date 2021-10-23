from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('posts/<int:pk>/like/', views.PostLike.as_view()),
    path('post-create/', views.PostCreate.as_view()),
    path('create-user/', views.CreateUser.as_view()),
    path('authenticate/', views.AuthenticateUser.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
