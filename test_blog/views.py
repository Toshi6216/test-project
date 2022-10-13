from django.shortcuts import render
from django.views.generic import FormView, TemplateView, ListView

from test_blog.models import SampleModel
from .forms import *
from django.urls import reverse_lazy

class HomeView(TemplateView):
    template_name = "test_blog/index.html"
    

class TestblogFormView(FormView):
    template_name = "test_blog/blog_form.html"
    form_class = TestblogFormClass
    success_url = reverse_lazy("test_blog:home")

    def form_valid(self, form):
        data = form.cleaned_data
        obj = SampleModel(**data)
        obj.save()
        return super().form_valid(form)

class BlogListView(ListView):
    template_name = "test_blog/index.html"
    model = SampleModel