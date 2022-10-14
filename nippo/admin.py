from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(NippoModel)
class NippoModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

@admin.register(ContentsCard)
class ContentsCardAdmin(admin.ModelAdmin):
    list_display = ('id','post', 'subtitle', 'content')
