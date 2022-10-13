from django.urls import path
from . import views

app_name = 'test_blog'

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('form/', views.TestblogFormView.as_view(), name="blog_form"),
]