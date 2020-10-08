from django.urls import path
from . import views
from .views import (PostListView,PostCreateView,PostUpdateView,PostDetailView,
                    PostDeleteView,UserPostListView,AuthorListView,post_search)

urlpatterns = [
    path('',PostListView.as_view(),name='blog-home'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    # path('post/<int:pk>/',PostDetail,name='post-detail'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('user/<str:username>',UserPostListView.as_view(),name='user-posts'),
    path('authors/',AuthorListView.as_view(),name='authors'),
    path('search/',post_search,name="post_search"),
]
