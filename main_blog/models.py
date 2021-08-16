from django.db import models
from django.db.models import Model
from django.utils import timezone
from django.conf import settings


class Post(models.Model):  # models.Modelはdjangoにデータベースに保存するべきだと伝えている。　# 下の5行がプロパティ（状態）を表している
    objects = None
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    text_article = models.TextField()
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(null=True, blank=True)

    def publish(self):  # 下の２つのメソッド（命令）を定義している　   ここでは何をしている？
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    post = models.ForeignKey('main_blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


def approved_comments(self):
    return self.comments.filter(approved_comment=True)


class Category(models.Model):
    category_url = models.SlugField(null=True, blank=True)
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name


