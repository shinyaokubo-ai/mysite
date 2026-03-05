from django.contrib import admin
from django.urls import path, include  # include を追加
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.urls')),
    
    # ここに追加！カッコの内側に入れるのが正解です
    path('google572018d7ddc4e357.html', lambda r: HttpResponse("google-site-verification: google572018d7ddc4e357.html", content_type="text/html")),
]



# 画像を表示するための設定（開発モード用）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


