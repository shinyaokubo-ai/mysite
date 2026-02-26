from django.urls import path
from . import views

urlpatterns = [
    # --- 表側のページ ---
    path('', views.IndexView.as_view(), name='index'),
    path('service/', views.ServiceView.as_view(), name='service'),
    # ▼▼▼ 新しく追加した詳細ページ ▼▼▼
    path('service/coating/', views.ServiceCoatingView.as_view(), name='service_coating'),
    path('service/wash/', views.ServiceWashView.as_view(), name='service_wash'),
    path('service/film/', views.ServiceFilmView.as_view(), name='service_film'),
    # ▲▲▲ 追加ここまで ▲▲▲


    path('works/', views.WorksView.as_view(), name='works'),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('blog/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('contact/', views.contact, name='contact'),
    path('company/', views.CompanyView.as_view(), name='company'),

    # --- 裏側のページ（管理者用ダッシュボード・Vue.js使用） ---
    path('manage/', views.DashboardView.as_view(), name='dashboard'),

    # --- 編集・新規・削除機能（サーバー側で処理） ---
    path('manage/create/', views.post_create, name='post_create'),
    path('manage/edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('manage/delete/<int:pk>/', views.post_delete, name='post_delete'),

    # --- API（Vue.jsがデータを取得するための専用URL） ---
    path('api/posts/', views.api_posts, name='api_posts'),
    path('api/posts/delete/<int:pk>/', views.api_post_delete, name='api_post_delete'),
    
]