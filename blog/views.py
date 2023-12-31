from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from rest_framework.permissions import AllowAny
from django.contrib import messages
from users import verify
from .forms import PostCreationForm

from .models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone

# Create your views here.


@api_view(['GET'])
@permission_classes([AllowAny])
@login_required()
def PostListView(request):
    posts = Post.objects.order_by('-date_posted')

    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/home.html', {"page_obj": page_obj,"is_paginated":True})

@api_view(['GET'])
@permission_classes([AllowAny])
@login_required()
def PostbyUserView(request,username):
    User = get_user_model()
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user).order_by('-date_posted')
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_by_user.html', {"page_obj": page_obj, "is_paginated": True,"username": username})

@api_view(['GET'])
@permission_classes([AllowAny])
@login_required()
def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

@api_view(['GET'])
@login_required()
def PostDetailView(request,id):
    data = Post.objects.get(id=id)
    return render(request, 'blog/post_detail.html', {'object': data})

@api_view(['GET','POST'])
@login_required()
def PostCreateView(request):
    if request.method == 'POST':
        if request.POST['author'] != str(request.user.id):
            messages.success(request,'permission denied , invalid user')
            return redirect('blog-home')
        form = PostCreationForm(request.POST)
        form_u = form.save(commit=False)
        form_u.date_posted = str(datetime.now())
        if form.is_valid():
            form_u.save()
            messages.success(request,f"added new blog")
            return redirect('blog-home')

    else:
        form = PostCreationForm()
    return render(request,'blog/post_form.html',{'form': form})


@api_view(['GET','POST'])
@login_required()
def PostUpdateView(request,id):

    if request.method == 'POST':
        if request.POST['author'] != str(request.user.id):
            messages.success(request,'permission denied , invalid user')
            return redirect('blog-home')
        curr_form = Post.objects.get(id=id)
        #form = PostCreationForm(instance=curr_form)
        form = PostCreationForm(request.POST,instance=curr_form)
        form_u = form.save(commit=False)
        form_u.date_posted = str(datetime.now())
        if form.is_valid():
            form.save()
            messages.success(request, f"blog updated")
            return redirect('blog-home')

    else:

        print(id)
        curr_form = Post.objects.get(id=id)
        form = PostCreationForm(instance=curr_form)

    return render(request, 'blog/post_form.html', {'form': form})

@api_view(['GET','POST'])
@login_required()
def PostDeleteView(request,id):
    post_to_delete = Post.objects.get(id=id)
    if request.method == 'POST':
        messages.success(request, f"blog \"{post_to_delete.title}\" is deleted")
        post_to_delete.delete()
    else:
        if post_to_delete.author_id != str(request.user.id):
            messages.success(request,'permission denied , invalid user')
            return redirect('blog-home')
        return render(request, 'blog/post_confirm_delete.html',{'object': post_to_delete})


    return redirect('blog-home')


# class PostListView(LoginRequiredMixin,ListView):
#     model = Post
#     template_name = 'blog/home.html'
#     context_object_name = 'posts'
#     ordering = ['-date_posted']
# class PostDetailView(LoginRequiredMixin, DetailView):
#     model = Post
# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     fields = ['title','content']
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)
# class PostUpdateView(UserPassesTestMixin, UpdateView):
#     model = Post
#     fields = ['title','content']
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)
#
#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.author:
#             return True
#         return False






