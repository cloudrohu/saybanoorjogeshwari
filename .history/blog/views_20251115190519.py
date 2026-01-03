from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Tag
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        qs = Post.objects.filter(status='published').order_by('-publish_date')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(excerpt__icontains=q) |
                Q(content__icontains=q) |
                Q(tags__name__icontains=q)
            ).distinct()
        cat = self.kwargs.get('category_slug')
        if cat:
            qs = qs.filter(category__slug=cat)
        tag = self.kwargs.get('tag_slug')
        if tag:
            qs = qs.filter(tags__slug=tag)
        return qs

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Post, slug=self.kwargs.get('slug'), status='published')
        # increment view count (simple)
        Post.objects.filter(pk=obj.pk).update(views=models.F('views') + 1)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(active=True)
        return context

from django import models as djmodels

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user or self.request.user.is_staff

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user or self.request.user.is_staff

# Comment submission view (function-based)
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

@require_POST
def post_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        # moderation: keep active False by default OR set True if you prefer auto-approve
        comment.active = False
        comment.save()
        # you may want to show a success message
    return redirect(post.get_absolute_url())
