from typing import Any
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, resolve_url
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db.models import Sum

from django.views.generic import ListView, DetailView, View, CreateView, TemplateView
from .forms import CommentaryCreationForm, PostCreateForm
from .models import Branch, Post, Commentary, Rating, Grade
from django.db.models import Sum
from .mixins import HavePermissionsMixin

# Create your views here.

def index(request):
    return HttpResponseRedirect(resolve_url('post-list'))

class BranchListView(ListView):
    model = Branch
    template_name = "forum/branch-list.html"
    context_object_name = 'branches'

class BranchDetailView(DetailView):
    model = Branch
    template_name = "forum/branch-detail.html"
    context_object_name = 'branch'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        _posts = self.get_object().posts.all()
        if self.request.GET.get('order_by') is None:
            _posts = _posts.order_by('-rating__sum_rating')
        else:
            _posts = _posts.order_by('-created')
        context['posts'] = _posts

        return context

class PostListView(ListView):
    model = Post
    template_name = "forum/post-list.html"
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        _posts = self.model.objects
        if self.request.GET.get('order_by') is None:
            _posts = self.model.objects.order_by('-rating__sum_rating')
        else:
            _posts = _posts.order_by('-created')
        context['posts'] = _posts

        return context

class PostDetailView(DetailView):
    model = Post
    template_name = "forum/post-detail.html"
    context_object_name = 'post'        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentaryCreationForm()
        post = self.get_object()

        _comments = Commentary.objects.filter(post=post, commentary__isnull=True)
        if self.request.GET.get('order_by') is None:
            _comments = _comments.order_by('-rating__sum_rating')
        else:
            _comments = _comments.order_by('-created')
        context['comments'] = _comments

        return context
    
class CommentDeleteView(HavePermissionsMixin, View):
    model = Commentary

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs.get('cr'))

    def post(self, request, *args, **kwargs):
        commentary = self.get_object()
        commentary.delete()

        return HttpResponseRedirect(commentary.post.get_absolute_url())

class CommentaryCreateView(LoginRequiredMixin, View):
    form_class = CommentaryCreationForm
    model = Commentary

    def get_post(self, **kwargs):
        post_id = self.kwargs.get('pk')
        return get_object_or_404(Post, pk=post_id)
    
    def get_comment(self, **kwargs):
        comment_id = self.kwargs.get('cr')
        return get_object_or_404(Commentary, pk=comment_id)
    
    def post(self, request, *args, **kwargs):
        comment_form = CommentaryCreationForm(request.POST, request.FILES)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)

            comment.author = request.user
            comment.post = self.get_post()
            if self.kwargs.get('cr'):
                comment.commentary = self.get_comment()
            comment.save()
            rating = Rating.objects.create()
            comment.rating = rating
            comment.save()
            return HttpResponseRedirect(comment.post.get_absolute_url())
        return render(request, "forum/comment-create.html", {'form': comment_form})
    
class PostDeleteView(LoginRequiredMixin, HavePermissionsMixin, View):
    model = Post

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        post_object = self.get_object()
        post_object.delete()

        return HttpResponseRedirect(post_object.branch.get_absolute_url())

class PostCreateView(LoginRequiredMixin, TemplateView):
    template_name = "forum/post-create.html"
    form_class = PostCreateForm
    model = Post

    def get_branch(self):
        return get_object_or_404(Branch, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostCreateForm()
        return context

    def post(self, request, *args, **kwargs):
        post_form = PostCreateForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_object = post_form.save(commit=False)

            post_object.author = request.user
            post_object.branch = self.get_branch()
            post_object.save()
            rating = Rating.objects.create()
            post_object.rating = rating
            post_object.save()
            return HttpResponseRedirect(post_object.get_absolute_url())
        return render(request, self.template_name, {'form': post_form})


class GradeCreateView(LoginRequiredMixin, View):
    model = Grade
    
    def post(self, request, *args, **kwargs):
        rating = Rating.objects.get(pk=request.POST.get('rating'))
        value = int(request.POST.get('value'))
        user = request.user if request.user.is_authenticated else None
        grade, created = self.model.objects.get_or_create(
            rating=rating,
            user = user,
            defaults={'value': value},
        )
        response = JsonResponse({'status': 'created', 'rating_sum': grade.rating.get_rating(), 'grade': grade.value})
        if not created:
            if grade.value == value:
                grade.delete()
                response = JsonResponse({'status': 'deleted', 'rating_sum': grade.rating.get_rating(), 'grade': 0})
            else:
                grade.value = value
                grade.user = user
                grade.save()
                response = JsonResponse({'status': 'updated', 'rating_sum': grade.rating.get_rating(), 'grade': grade.value})
    
        rating.sum_rating = rating.get_rating()
        rating.save()
        return response
    
def get_rating_view(request):
    if request.user.is_authenticated:
        rating = Rating.objects.get(pk=request.GET.get('rating'))
        grade = rating.grades.all().filter(user=request.user).last()
        if grade:
            return JsonResponse({'grade': grade.value})
    return JsonResponse({'grade': 0})

def set_dark_theme(request):
    request.session['theme'] = 'dark'

    previous_url = request.META.get('HTTP_REFERER')
    if previous_url:
        return HttpResponseRedirect(previous_url)
    return HttpResponseRedirect('/')

def set_light_theme(request):
    request.session['theme'] = 'light'

    previous_url = request.META.get('HTTP_REFERER')
    if previous_url:
        return HttpResponseRedirect(previous_url)
    return HttpResponseRedirect('/')