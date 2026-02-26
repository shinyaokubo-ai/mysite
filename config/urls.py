from django.contrib import admin
from django.urls import path, include  # include を追加
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # webアプリのURLを読み込む
    path('', include('web.urls')),
]

# 画像を表示するための設定（開発モード用）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)