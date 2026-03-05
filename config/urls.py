from django.contrib import admin
from django.urls import path, include  # include を追加
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView




urlpatterns = [
    path('admin/', admin.site.urls),
    # webアプリのURLを読み込む
    path('', include('web.urls')),
]


path('google572018d7ddc4e357.html', TemplateView.as_view(template_name='googleXXXXXXXX.html', content_type='text/html')),

# 画像を表示するための設定（開発モード用）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


