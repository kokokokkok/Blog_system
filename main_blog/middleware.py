from .models import Category,Post  # ここでは処理にフックを入れる、フックとは何かの処理をする前にしてほしい処理を割り込ませることのこと


class categorize:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # リクエストへの前処理を記述
        # request.cateに、Categoryモデルからブログ情報を取得する
        request.cate = Category.objects.all()  # この行以外はすべて基本構文

        # 固定
        response = self.get_response(request)

        # レスポンスへの後処理を記述

        return response
