from django.contrib import admin
from .models import Post

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