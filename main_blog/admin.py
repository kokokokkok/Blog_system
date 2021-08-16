from django.contrib import admin
from .models import Post, Comment, Category

# formsから定義された編集、管理したいものを渡してもらっている。

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
