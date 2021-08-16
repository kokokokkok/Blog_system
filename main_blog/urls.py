from django.urls import path
from . import views

# htmlでurlを指定するときはここを通して行う,urlを作るときなのでここにあるurlはサイト内すべてのurlに等しい

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('contact/', views.contact, name="contact"),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),  # ”post/整数” がurlとして撃ち込まれたら、viewの中のpost_listを返しす！
    path('post/new/', views.post_new, name='post_new'),
    # <int:pk> – この部分はトリッキーです。これはDjangoは整数の値を期待し、その値がpkという名前の変数でビューに渡されることを意味しています。
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<slug>/publish/', views.post_publish, name='post_publish'),
    path('post/<slug>/remove/', views.post_remove, name='post_remove'),
    path('post/<slug:slug>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/article/<slug:slug>/', views.post_article, name='post_article'),  # textでart_urlを分だと認識させれる？
    path('post/article/<slug:slug>', views.category, name='category'),
]
