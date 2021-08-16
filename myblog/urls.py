from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),  # ここの'admin/'を変えておかないと簡単に管理サイトのurlを特定される。
    path('accounts/login/', views.LoginView.as_view(), name='login'),  # ログイン機能を作ってくれる
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', include('main_blog.urls')),  # ここでappのurlとつなげる。
]
