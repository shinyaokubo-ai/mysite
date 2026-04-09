from django.contrib import admin
from .models import Post, Contact # 🌟 Contactを追加

# 管理画面にPostモデルを登録する
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 一覧画面で見せる項目
    list_display = ('id', 'title', 'category', 'status', 'created_at')
    # リンクをクリックして編集画面に行く項目
    list_display_links = ('id', 'title')
    # フィルター機能（右側に出るやつ）
    list_filter = ('category', 'status')
    # 検索機能
    search_fields = ('title', 'content')

# 🌟 追加：管理画面でお問い合わせを一覧で見やすくする設定
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin): # ← ここを静かに修正しました！
    list_display = ('created_at', 'name', 'email', 'car_model') # 一覧に出す項目
    search_fields = ('name', 'email', 'car_model') # 検索機能