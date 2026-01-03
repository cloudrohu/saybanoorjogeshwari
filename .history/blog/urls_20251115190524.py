from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('category/<slug:category_slug>/', views.PostListView.as_view(), name='category_posts'),
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='tag_posts'),
    path('post/add/', views.PostCreateView.as_view(), name='post_add'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<slug:slug>/comment/', views.post_comment, name='post_comment'),
]
