from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Article, Comment, Category
from django.urls import reverse_lazy
from .forms import CommentForm
from .filter import CommentFilter
import django.dispatch
from django.contrib.auth.decorators import login_required


def home(request):
    context = {
        'article': Article.objects.all()
    }
    return render(request, 'project/home.html', context)


class PostListView(ListView):
    model = Article

    # <app>/<model>_<viewtype>.html
    template_name = 'project/home.html'

    # this variable <context_object_name> is passed to the template --> home.html
    context_object_name = 'article_0'
    ordering = ['-date_created']

    paginate_by = 2


class UserPostListView(ListView):
    model = Article
    # <app>/<model>_<viewtype>.html
    template_name = 'project/user_posts.html'
    # this variable <context_object_name> is passed to the template --> home.html
    context_object_name = 'article_0'
    ordering = ['-date_created']
    paginate_by = 2

    def get_queryset(self):
        # username is passed from url
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Article.objects.filter(author=user).order_by('-date_created')


class PostDetailView(DetailView):
    model = Article


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'text', 'category', 'upload']

    def form_valid(self, form):
        form.instance.author = self.request.user  # self.object = form.save()
        return super().form_valid(form)  # return super().form_valid(form)

    success_url = reverse_lazy('home')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    # fields = '__all__'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.article_id = self.kwargs['pk']
        form.instance.username = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('profile')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'text', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        article = self.get_object()
        # checking if the current user is the author of the post.
        if self.request.user == article.author:  # self.request.user --> current user in the browser
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = '/profile'

    # checking if the user is an author
    def test_func(self):
        article = self.get_object()
        # checking if the current user is the author of the post.
        if self.request.user == article.author:  # self.request.user --> current user in the browser
            return True
        return False


class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    # <app>/<model>_<viewtype>.html
    template_name = 'project/comment_list.html'
    context_object_name = 'comments' # we use it in template as {% for comment in comments %}
    ordering = ['-date_added']
    paginate_by = 3
    # form_class = CommentForm
    myFilter = CommentFilter()

    def get_queryset(self):
        user_id = self.request.user.id # get logged-in user id because he is an author of his own posts
        return Comment.objects.filter(article__author_id=user_id).order_by('-date_added')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CommentFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('comment_list')


accepted = django.dispatch.Signal()


def accept(request, **kwargs):

    accepted.send(sender=Comment.__class__, **kwargs) # sending signal, where Comment model is sender argument
        # means that any changes with Comment model will send signal
    return redirect('/home/comments')


@login_required
def subscribe(request, **kwargs):
    print(kwargs['pk'])
    pk = kwargs['pk']  # 0 то же самое можно записать, как: pk = kwargs.get('pk')

    my_post = Article.objects.get(id=pk).category
    print(my_post)

    # находим объекты категории, с которыми связан данный пост,
    # и добавляем текущего пользователя в поле subscribers моделей
    Category.objects.get(id=my_post.id).subscribers.add(request.user)

    subscribers = Category.objects.filter(subscribers=request.user)
    print(f"subscribed categories={subscribers.values()}")
    #

    print('Эта новость относится к категории:', subscribers.last())
    print(subscribers)

    print('Вы подписаны на следующие категории: ', end='')
    for i in Article.objects.filter(category__subscribers=request.user.id): print(i, end='    ')
    print("")
    return redirect('/')
