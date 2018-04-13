from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from .models import Post, PostNew
from .forms import PostForm
from django.utils import timezone
from django.shortcuts import redirect
from cassandra.cluster import Cluster

#Adding by Yi
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.views import login, logout
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    post_list = Post.objects.all()
    return render(request, 'home.html', {
        'post_list': post_list,
    })

def login_form(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            # auth.login(request, user)
            #return redirect('/website/profile/')
            return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request,'login_form.html',{'form':form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # auth.login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_form(request):
    logout(request)
    posts = PostNew.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'post_list_without_edit.html', {'posts': posts})


def post_list(request):
    posts = PostNew.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'post_list.html', {'posts': posts})

def post_list_without_edit(request):
    posts = PostNew.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'post_list_without_edit.html', {'posts': posts})

def post_detail_without_edit(request, pk):
    post = get_object_or_404(PostNew, pk=pk)
    return render(request, 'post_detail_without_edit.html', {'post': post})


def post_detail(request, pk):
    post = get_object_or_404(PostNew, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.author = request.user
            post.published_date = timezone.now()
            post.save()
            cluster = Cluster(['127.0.0.1'])
            session = cluster.connect()
            print("INSERT INTO ezcook17.recipe (id, content, owner, title) VALUES (now(),'"+str(post.text)+"', '"+str(request.user)+"', '"+str(post.title)+"');")
            session.execute("INSERT INTO ezcook17.recipe (id, content, owner, title) VALUES (now(),'"+str(post.text)+"', '"+str(request.user)+"', '"+str(post.title)+"');")
            # session.execute("INSERT INTO ezcook17.recipe (id, content, owner, title) VALUES (now(),"+str(post.text)+", "+str(request.user)+", "+str(post.title)+");")
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_new.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(PostNew, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            #post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})