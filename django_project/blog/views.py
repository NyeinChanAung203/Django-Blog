from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Comment
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User 
from .forms import CommentForm,SearchForm
# Create your views here.
from hitcount.views import HitCountDetailView
from django.db.models import Q


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

   
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context.update({
        'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context


class UserPostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# @login_required
# def PostDetail(request,pk):
#     post = get_object_or_404(Post,pk=pk)
#     comments = post.comments.filter(active=True)
#     new_comment = None
#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.post = post
#             new_comment.user = request.user
#             new_comment.save()
#     else:
#         comment_form = CommentForm()
#     template_name = 'blog/detail.html'
#     context = {'post':post,'comments':comments,'new_comment':new_comment,'comment_form':comment_form,
#                 'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],}
#     return render(request,template_name,context)

class PostDetailView(LoginRequiredMixin,HitCountDetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    count_hit = True

        
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        comment_form = CommentForm()
        post = get_object_or_404(Post,pk=self.object.pk )
        comments = post.comments.filter(active=True)
        new_comment = None
        context.update({
        'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        'comment_form':comment_form,'new_comment':new_comment,'comments':comments,
        })
        return context

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        post = get_object_or_404(Post,pk=kwargs['pk'])
        comments = post.comments.filter(active=True)
        new_comment = None
        if self.request.method == 'POST':
            comment_form = CommentForm(data=self.request.POST)
            context = super(PostDetailView,self).get_context_data(**kwargs)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.user = self.request.user
                new_comment.save()
                context['new_comment'] = new_comment
                
        context['popular_posts'] = Post.objects.order_by('-hit_count_generic__hits')[:3]
        context['comments'] = comments
        return self.render_to_response(context=context)





class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = 'blog/create.html'
    fields = ['title','content']
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    template_name = 'blog/create.html'
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    context_object_name = 'post'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class AuthorListView(ListView):
    model = User
    context_object_name = 'authors'
    paginate_by = 10
    template_name = 'blog/authors.html'

    def get_queryset(self):
        return User.objects.exclude(id=1).order_by('username')

def post_search(request):
	form = SearchForm()
	query = None
	results = []
	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data['query']
			lookup = Q(title__icontains=query) | Q(content__icontains=query)
			posts = Post.objects.all()
			results = posts.filter(lookup).distinct()
	template_name = 'blog/search.html'
	context = {'form':form,'query':query,'results':results}
	return render(request,template_name,context)