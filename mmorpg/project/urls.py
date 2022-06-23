from django.urls import path
from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, CommentCreateView, CommentListView, CommentDeleteView, accept, subscribe,)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('home/<int:pk>/', PostDetailView.as_view(), name='article-detail'),
    path('home/new/', PostCreateView.as_view(), name='article-create'),
    path('home/<int:pk>/comment', CommentCreateView.as_view(), name='comment_create'),
    path('home/comments', CommentListView.as_view(), name='comment_list'),
    path('home/<int:pk>/update/', PostUpdateView.as_view(), name='article-update'),
    path('home/<int:pk>/delete/', PostDeleteView.as_view(), name='article-delete'),
    path('home/comments/<int:pk>/accept', accept, name='comment-accept'),
    path('home/comments/<int:pk>/delete', CommentDeleteView.as_view(), name='comment-delete'),
    path('<int:pk>/subscribe', subscribe, name='article-subscribe'),
]