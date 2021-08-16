from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .forms import PostForm, CommentForm
from .models import Post, Category


# viewでは　（１、urlとhtmlのファイルを結びつける）　、（２、htmlに必要なデータをmodelから取り出すか定義してhtmlファイルに送る）
# (３、htmlで入力されたデータを処理する＝処理とhtmlの表示をセットとして考える)

def category(request, slug):  # 表示させる記事の選定を行う、（Category内のcategory_urlを利用 ）表示させる記事が入っていいる変数を渡す（Post内）
    url = get_object_or_404(Category, category_url=slug)
    category_url = Post.objects.filter(slug__startswith=url.category_url).order_by('published_date') #filterをかけてる
    paginator = Paginator(category_url, 7)
    p = request.GET.get('p')
    category_url_articles = paginator.get_page(p)
    return render(request, 'main_blog/category_posts.html', {'category_url_articles': category_url_articles})


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        '-published_date')  # post_list.html に送りたいデータの定義をしている,
    paginator = Paginator(posts, 7)  # 1ページに2件表示
    p = request.GET.get('p')  # URLのパラメータから現在のページ番号を取得
    articles = paginator.get_page(p)  # 指定のページのArticleを取得

    return render(request, 'main_blog/post_list.html',
                  {'articles': articles})  # post_list.htmlでpostsというデータを表示できるように送っている！


def post_detail(request, slug):  # requestとpkをインプットする
    post = get_object_or_404(Post, slug=slug)

    return render(request, 'main_blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)  # 編集されたデータがある場合すべてをセーブして保存し、post_detailに飛ばす！
        if form.is_valid():
            post = form.save(commit=False)  # "title"と"text"のデータの保存まで行っている
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
        return render(request, 'main_blog/post_edit.html', {'form': form})  # 編集されたデータのない最初の段階は有無を言わさずpost_editにとばす！


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)  # 既に入力済みのデータを入れる
    if request.method == "POST":  # 編集されたかを、確認
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'main_blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'main_blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.publish()
    return redirect('post_detail', slug=slug)


def publish(self):
    self.published_date = timezone.now()
    self.save()


@login_required
def post_remove(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_article', slug=slug)
    else:
        form = CommentForm()
    return render(request, 'main_blog/add_comment_to_post.html', {'form': form})


def contact(request):
    return render(request, 'main_blog/contact.html')


def post_article(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save()

    count = slug.split('-')[0]  # ここで記事のurlの　－　以降を消してfilterで検索している　
    # ここでめちゃくちゃ時間かかったけど、思いもよらない解決法で解決できたので、プログラミングで壁にぶつかったときはやってもらいたい処理を分解して指示する ！！
    relate_url = Post.objects.filter(slug__istartswith=count).order_by('-views')
    # ここにworksなどのcategory_urlの特定されたものが必要

    return render(request, 'main_blog/post_article.html',
                  {'post': post, 'relate_url': relate_url})  # post_article.html内の中身（記事）を拡張機能で次足していけばいい
