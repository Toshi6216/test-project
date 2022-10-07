from sre_constants import SUCCESS
from django.shortcuts import render,  redirect
from random import randint
from .models import *
from django.views.generic import View, CreateView
from .forms import PostForm, Formset, NippoFormClass
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

def nippoListView(request):
    template_name = "nippo/nippo-list.html"
    ctx={}
    qs = NippoModel.objects.all()
    ctx["object_list"] = qs
    
    if request.GET:
        number = request.GET["number"]
        return redirect("lucky", number )

    return render(request, template_name, ctx)

def nippoLuckyView(request, number):
    template_name = "nippo/nippo-lucky.html"
    random_int = randint(1,10)
    ctx = {
        "random_int": random_int,
        "number" : number,
    }
    return render(request, template_name, ctx)

def nippoCreateView(request):
    template_name = "nippo/nippo-form.html"

    if request.POST:
        title = request.POST["title"]
        content = request.POST["content"]
        #受け取った値で処理
        print(title,content)
        obj = NippoModel(
            title = title, 
            content = content
        )
        obj.save()

    return render(request, template_name)

def new_nippoCreateView(request):
    template_name="nippo/new-nippo-form.html"

    form = NippoFormClass(request.POST or None)
    ctx = {'form':form}

    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        obj = NippoModel(title=title, content=content)
        obj.save()

    return render(request, template_name, ctx)

    

def nippoDetailView(request, pk):
    template_name = "nippo/nippo-detail.html"
    ctx = {}
    q = NippoModel.objects.get(pk=pk)
    ctx["object"] = q
    return render(request, template_name, ctx)
    
#以下、お試し用

#ブログの一覧
class BlogIndexView(View):
    #このviewがコールされたら最初にget関数が呼ばれる
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id') #新しいものから順番に並べる
        return render(request, 'blog-index.html',{
            'post_data': post_data
        })

#記事詳細画面のview
class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk']) #pkで記事を特定してデータ取得
        return render(request, 'post_detail.html',{
            'post_data': post_data
        })

#ブログ投稿
class CreatePostView(View,LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        formset = Formset(request.POST or None)
        context = {
            'form' : form,
            'formset' : formset
            }
        return render(request, 'post_form.html', context)

    def post(self, request, *args, **kwargs): #投稿内容をデータベースに保存
        form = PostForm(request.POST or None)
        context = {'form' : form }
        #フォームのバリデーション
        if form.is_valid():
            post = form.save(commit=False)
            formset = Formset(request.POST, instance=post)
            if formset.is_valid():
                post.save()
                formset.save()
                return redirect('blog-index')
        else:
            context['formset'] = formset

        return render(request, 'post_form.html', context)
    

        


    