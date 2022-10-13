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

 
#ブログ投稿
class CreatePostView(CreateView,LoginRequiredMixin):
    template_name='post_form.html'
    #form_class = PostForm
    queryset = Post.objects.all()
    #queryset = ContentsCard.objects.all()
    fields = '__all__'
    
    def get_success_url(self):
        return reverse("blog-index")

    #def get(self, request, *args, **kwargs):
    def get_context_data(self, **kwargs):
        ctx = super(CreatePostView, self).get_context_data(**kwargs)

        if self.request.method=="POST":
            ctx["blog_formset"] = CardFormset(self.request.POST)
        else:
            ctx["blog_formset"] = CardFormset()
        return ctx
    

    def form_valid(self, form):
        ctx = self.get_context_data()
        blog_formset = ctx["blog_formset"]
        if blog_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.title = self.request.title
            self.object.save()

            blog_formset.instance = self.object
            blog_formset.save()

            return redirect('blog-index')
        else:
            ctx["form"] = form
            return self.render_to_response(ctx)


#ブログ投稿
#class CreatePostView(CreateView,LoginRequiredMixin):
#    template_name = "post_form.html"
#    form_clas = PostForm
#    def get_success_url(self):
#        return reverse("post_detail", kwargs={"pk": self.object.id})

#    def get_context_data(self, **kwargs):
#        ctx = super(CreatePostView, self).get_context_data(**kwargs)
#        if self.request.method == "POST":
#            ctx["formset"] = FormSet(self.request.POST, self.request.FILES)
#        else:
#            ctx["formset"] = FormSet()
#        return ctx

#    def form_valid(self, form):
#        ctx = self.get_context_data()
#        formset = ctx["formset"]
#        if formset.is_valid():
#            self.object = form.save(commit=False)
#            self.object.user = self.request.user
#            self.object.save()

            # FormSet の内容を保存
 #           formset.instance = self.object
 #           formset.save()

 #           return redirect(self.get_redirect_url())
 #       else:
 #           ctx["form"] = form
 #           return self.render_to_response(ctx)

 #   def get(self, request, *args, **kwargs):
 #       form = PostForm(request.POST or None)
 #       post_formset = Formset(request.POST or None)
 #       context = {
 #           'form' : form,
 #           'post_formset' : post_formset
 #           }
        
        #return render(request, 'post_form.html', context)
 #       return super().form_valid(form)

#    def post(self, request, *args, **kwargs): #投稿内容をデータベースに保存
#        form = PostForm(request.POST or None)
#        context = {'form' : form }
        #フォームのバリデーション
#        if form.is_valid():
#            post = form.save(commit=False)
#            post_formset = Formset(request.POST, instance=post)
#            if post_formset.is_valid():
                
#                post.save()
#                post_formset.save()
               
#                return redirect('blog-index')
#        else:
#            context['post_formset'] = post_formset
#        return render(request, 'post_form.html', context)




        


    