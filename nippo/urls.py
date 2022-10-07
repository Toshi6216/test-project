from django.urls import path
from .views import *

urlpatterns = [
    
    path('', nippoListView, name="index"),
    path('lucky/<int:number>/', nippoLuckyView, name="lucky"),
    path('form/', nippoCreateView, name="form"),
    path('detail/<int:pk>/', nippoDetailView, name="detail"),
    path('newform/', new_nippoCreateView, name="new_form"),

    path('post/', BlogIndexView.as_view(), name="blog-index"),
    path('post/<int:pk>/detail/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', CreatePostView.as_view(), name='post_form'),
]
