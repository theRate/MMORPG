from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from .filters import ResponseFilter
from .forms import PostForm, ResponseForm
from .models import Post, Response
from .tasks import notify_approved_response, notify_new_response


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'infoboard/home.html'
    context_object_name = 'posts'
    ordering = '-date_u'
    paginate_by = 3


class PostDetailView(DetailView, CreateView):
    model = Post
    form_class = ResponseForm
    template_name = 'infoboard/post.html'
    context_object_name = 'post'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.author = User.objects.get(id=self.request.user.id)
        response.post = Post.objects.get(id=self.kwargs.get('pk'))
        response.save()
        notify_new_response(response.id)
        return redirect('home')


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'infoboard/addpost.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = User.objects.get(id=self.request.user.id)
        post.save()
        return redirect('home')


class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    template_name = 'infoboard/updatepost.html'

    def get_object(self, **kwargs):
        id_id = self.kwargs.get('pk')
        return Post.objects.get(pk=id_id)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user == Post.objects.get(pk=self.kwargs.get('pk')).author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse('ACCESS DENIED! Изменять или удалять обьявление может только его автор!')


class PostDeleteView(DeleteView):
    template_name = 'infoboard/deletepost.html'
    queryset = Post.objects.all()
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user == Post.objects.get(pk=self.kwargs.get('pk')).author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse('ACCESS DENIED! Изменять или удалять обьявление может только его автор!')


class ResponseListView(ListView):
    model = Response
    template_name = 'infoboard/checkresps.html'
    context_object_name = 'responses'

    def get_queryset(self):
        return super().get_queryset().filter(post_id__author_id=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ResponseFilter(self.request.GET, queryset=self.get_queryset())
        return context


def approve_response(*args, **kwargs):
    response = Response.objects.get(id=kwargs.get('pk'))
    response.approved = True
    response.save()
    notify_approved_response(response.id)
    return redirect('checkresps')


def delete_response(*args, **kwargs):
    response = Response.objects.get(id=kwargs.get('pk'))
    response.delete()
    return redirect('checkresps')
