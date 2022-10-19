from sre_constants import SUCCESS
from django.shortcuts import render,  redirect
from random import randint
from .models import *
from django.views.generic import View, CreateView
from .forms import PostForm, CardFormset, NippoFormClass
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.urls import reverse

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

FORM_NUM = 1 #フォーム数
FORM_VALUES = {} #前回のPOST時のフォーム情報を格納
#ブログ投稿
class CreatePostView(CreateView,LoginRequiredMixin):
    template_name='post_form.html'
    form_class = PostForm
    
    
    def get_success_url(self):
        return reverse("blog-index")
        
    def get_form_kwargs(self):
        # デフォルトのget_form_kwargsメソッドを呼び出す
        kwargs = super().get_form_kwargs()
        # FORM_VALUESが空でない場合（入力中のフォームがある場合）、dataキーにFORM_VALUESを設定
        if FORM_VALUES:
            kwargs['data'] = FORM_VALUES
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        global FORM_NUM
     #   global FORM_VALUES
        # 追加ボタンが押された時の挙動
        

        if self.request.method=="POST":
            if "btn_submit" in self.request.POST:
                post_formset = self.request.POST.copy()
                files= self.request.FILES
               # post_formset['contentscard-TOTAL_FORMS'] = 1
                post_formset['contentscard-TOTAL_FORMS'] = FORM_NUM
                post_formset['contentscard-INITIAL_FORMS'] = 0
                ctx["blog_formset"] = CardFormset(post_formset,files)

            if "btn_add" in self.request.POST:
                FORM_NUM += 1    # フォーム数をインクリメント
            #    FORM_VALUES = self.request.POST.copy()  # リクエストの内容をコピー
                
                FORM_VALUES['contentscard-TOTAL_FORMS'] = FORM_NUM   # フォーム数を上書き
                ctx["blog_formset"] = CardFormset(FORM_VALUES)
            return ctx

        else:
            ctx["blog_formset"] = CardFormset()
        return ctx

    def form_valid(self, form):
        
        ctx = self.get_context_data()
        blog_formset = ctx["blog_formset"]
        
        if blog_formset.is_valid():
            
            self.object=form.save(commit=False)
            self.object.author=self.request.user
            
            self.object.save()
            blog_formset.instance = self.object
            blog_formset.save()

            return redirect(self.get_success_url())
        else:
            ctx["form"] = form
            return self.render_to_response(ctx)






        


    