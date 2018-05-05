from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from .models import Post
from .models import Comment
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse

# def index(request):
#     return HttpResponse("Hello, world. This is where you will soon be able to interact with a post interface.")
# Create your views here.

@login_required
def dashboard(request):
    posts = Post.objects.all().order_by('-pud_date')
    comments = Comment.objects.all().order_by('-pud_date')
    return render(request, 'dashboard.html', {'section': 'dashboard', 'posts':posts, 'comments':comments})

def view_sort(request, username):
    # posts = Post.objects.all()
    username = username
    # author = Post.user
    print(username)
    posts = Post.objects.all().filter(user__username=str(username))
    length = len(posts)
    return render(request, 'posts.html', {'posts': posts, 'username':username, 'length':length})

# class CreateMyModelView(CreateView):
#     model = MyModel
#     form_class = MyModelForm
#     template_name = 'myapp/template.html'
#     success_url = 'myapp/success.html'

@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pud_date = timezone.now()
            post.user = request.user
            post.save()
            return redirect('{}#mostrecent'.format(reverse('dashboard')))
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.pub_date = timezone.now()
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('{}#post{}'.format(reverse('dashboard'), pk))
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form, 'post':post})

def user_author_check(author, user):
    return author == user

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if user_author_check(post.user, request.user):
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('{}#post{}'.format(reverse('dashboard'), pk))
        else:
            form = PostForm(instance=post)
        return render(request, 'add_post.html', {'form': form, 'post': post})
    else:
        return HttpResponse("You do not have permission to edit this post.")

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if user_author_check(post.user, request.user):
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            post.delete()
            return redirect('{}#mostrecent'.format(reverse('dashboard')))
        else:
            form = PostForm(instance=post)
        return render(request, 'add_post.html', {'form': form, 'post': post})
    else:
        return HttpResponse("You do not have permission to delete this post.")

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if user_author_check(comment.user, request.user):
        if request.method == "POST":
            form = CommentForm(request.POST, instance=comment)
            comment.delete()
            return redirect('{}#mostrecent'.format(reverse('dashboard')))
        else:
            form = CommentForm(instance=comment)
        return render(request, 'add_comment_to_post.html', {'form': form, 'comment': comment})
    else:
        return HttpResponse("You do not have permission to delete this post.")

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if user_author_check(comment.user, request.user):
        if request.method == "POST":
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('{}#comment{}'.format(reverse('dashboard'), pk))
        else:
            form = CommentForm(instance=comment)
        return render(request, 'add_comment_to_post.html', {'form': form, 'comment': comment})
    else:
        return HttpResponse("You do not have permission to edit this comment.")
