from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import PostForm, IngredientForm
from .models import UserModel, RecipeModel, IngredientModel
from django.utils import timezone
from django.shortcuts import redirect
from cassandra.cluster import Cluster
from cassandra.query import dict_factory

#Adding by Yi
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.views import login, logout
from django.contrib.auth.forms import AuthenticationForm

import uuid
from datetime import datetime

def login_form(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request,'login_form.html',{'form':form})


def signup(request):
    if request.method == 'POST':
        print("get post")
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user_model = UserModel.objects.create(username=username, password=raw_password)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list_without_edit')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_form(request):
    logout(request)
    return redirect('post_list_without_edit')

def post_list_without_edit(request):
    posts = RecipeModel.objects.all()
    return render(request, 'post_list_without_edit.html', {'posts': posts})
#
def post_detail_without_edit(request, pk):
    post = get_object_or_404(RecipeModel, id=uuid.UUID(pk))
    return render(request, 'post_detail_without_edit.html', {'post': post})

def post_detail(request, pk):
    post = get_object_or_404(RecipeModel, id=uuid.UUID(pk))
    user = UserModel.objects.filter(username=str(request.user)).get()
    user_ingred = user.stock
    post_ingred = post.ingredients
    shop_ingred = []
    for i in post_ingred:
        if i not in user_ingred:
            shop_ingred += i
    print(shop_ingred)
    post.shop_ingred = shop_ingred
    return render(request, 'post_detail.html', {'post': post})

def post_list(request):
    print("Hey this is post list")
    posts = RecipeModel.objects.all()
    post_list = []
    for model in posts:
        post_list.append(model)
    post_list.sort(key=lambda post: post.post_time, reverse=True)
    return render(request, 'post_list.html', {'posts': post_list})

def post_new(request):
    if request.method == "POST":
        myDict = dict(request.POST.iterlists())
        title = myDict['title'][0]
        content = myDict['content'][0]
        ingred_list = myDict['ingred[]']
        amount_list = myDict['amount[]']
        ingredients = {}
        for i, a in zip(ingred_list, amount_list):
            if i != "":
                ingredients[i] = a
        Rid = uuid.uuid1()
        post_model = RecipeModel.objects.create(id = Rid, title=title, content=content, owner=str(request.user), post_time=datetime.now(), ingredients=ingredients)
        for item in ingred_list:
            if IngredientModel.objects.filter(name=str(item)):
                ingred = IngredientModel.objects.filter(name=str(item)).get()
                ingred_usedby = ingred.usedby
                ingred_usedby.append(Rid)
                IngredientModel.objects(id=ingred.id, name=item).update(usedby=ingred_usedby)
            else:
                ingred_usedby = []
                ingred_usedby.append(Rid)
                IngredientModel.objects.create(id = uuid.uuid1(), name=item, usedby=ingred_usedby)
        return redirect('post_detail', pk=str(post_model.pk))
    else:
        form = PostForm()
    return render(request, 'post_new.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(RecipeModel, id=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            update_post = form.save(commit=False)
            post.title = update_post.title
            post.content = update_post.content
            post.post_time = datetime.now()
            post.save()

            for item in post.ingredients:
                if IngredientModel.objects.filter(name=str(item)):
                    ingred = IngredientModel.objects.filter(name=str(item)).get()
                    ingred_usedby = ingred.usedby
                    ingred_usedby.append(Rid)
                    IngredientModel.objects(id=ingred.id, name=item).update(usedby=ingred_usedby)
                else:
                    ingred_usedby = []
                    ingred_usedby.append(Rid)
                    IngredientModel.objects.create(id = uuid.uuid1(), name=item, usedby=ingred_usedby)

            return redirect('post_detail', pk=str(post.pk))
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})

def my_stock(request):
    user = UserModel.objects.filter(username=str(request.user)).get()
    ingredients = user.stock
    print(type(ingredients))
    print("my ingredients: {}".format(ingredients))
    return render(request, 'my_stock.html', {'ingredients': ingredients})

def add_ingredient(request):
    user = UserModel.objects.filter(username=str(request.user)).get()
    ingredients = user.stock
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['name'])
            ingredient_name = form.cleaned_data['name']
            ingredient_amount = form.cleaned_data['amount']
            ingredients[ingredient_name] = ingredient_amount
            user.save()
            return redirect('my_stock')
    else:
        form = IngredientForm()
    return render(request, 'add_ingredient.html', {'form': form, 'ingredients': ingredients})

# def edit_ingredient(request, name):
#     user = UserModel.objects.filter(username=str(request.user)).get()
#     ingredients = user.ingredients
#     ingred
#     # print(ingred.name)
#     if request.method == "POST":
#         # form = PostForm(request.POST, instance=post)
#         form = IngredientForm(request.POST, instance=ingred)
#         print(form)
#         form.name = name
#         if form.is_valid():
#             ingredient = form.save(commit=False)
#             ingredient.save()
#             print(type("{now():{}}"))
#             # cluster = Cluster(['18.219.216.0'])
#             # session = cluster.connect()
#             # ingred_map = "{'"+str(ingredient.name)+"':"+str(ingredient.amount)+"}"
#             # sql = "update ezcook17.user set ingredients = ingredients + {} where id = 1 and username = '{}'".format(ingred_map, str(request.user))
#             # print(sql)
#             # session.execute(sql)
#             return redirect('my_stock')
#     else:
#         form = IngredientForm()
#     return render(request, 'edit_ingredient.html', {'form': form})
