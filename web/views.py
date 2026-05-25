import re # 🌟スパム対策用
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.decorators import login_required

# 🌟 SystemSetting を追加し、綺麗にまとめました
from .models import Post, Contact, SystemSetting

# --- 1. 表側のページ（一般の人が見る画面） ---

class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 施工事例(Works)とブログ(Blog)の最新3件をトップページに送る
        context['works_posts'] = Post.objects.filter(category='Works', status='Published').order_by('-created_at')[:3]
        context['blog_posts'] = Post.objects.filter(category='Blog', status='Published').order_by('-created_at')[:3]
        return context

class ServiceView(TemplateView):
    template_name = 'service.html'

class ServiceCoatingView(TemplateView):
    template_name = 'service_coating.html'

class ServiceWashView(TemplateView):
    template_name = 'service_wash.html'

class ServiceFilmView(TemplateView):
    template_name = 'service_film.html'

class WorksView(TemplateView):
    template_name = 'works.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(category='Works', status='Published').order_by('-created_at')
        return context

class BlogView(TemplateView):
    template_name = 'blog.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(category='Blog', status='Published').order_by('-created_at')
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # 本文中の [video] を動画プレイヤー(HTMLタグ)に置き換える処理
        if post.image and (".mp4" in post.image.url.lower() or ".mov" in post.image.url.lower()):
            video_tag = f'<video src="{post.image.url}" class="video-player" controls preload="auto" playsinline></video>'
            
            if "[video]" in post.content:
                post.content = post.content.replace("[video]", video_tag)
            else:
                post.content += f"<br><br>{video_tag}"
        
        context['post'] = post
        return context

def contact(request):
    # 🌟 システム設定をデータベースから取得（なければ自動で作る）
    setting, created = SystemSetting.objects.get_or_create(id=1)

    # 🌟 緊急モードがONの場合は、送信処理をすべてスキップして画面を表示する
    if setting.is_emergency_form:
        return render(request, 'contact.html', {'setting': setting})

    if request.method == 'POST':
        # フォームから送られてきたデータをすべて受け取る
        user_name = request.POST.get('name')
        user_email = request.POST.get('email')
        user_phone = request.POST.get('phone')
        car_model = request.POST.get('car_model')
        car_color = request.POST.get('car_color')
        user_message = request.POST.get('message') or ""

        # 🌟【スパム対策】消えていたコードを復活させています！
        if not re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', user_message):
            return render(request, 'contact.html', {
                'error': 'お問い合わせの送信に失敗しました。内容を日本語で入力してください。',
                'setting': setting
            })

        # 🌟 0. データベース（Neon）に保存する（これが最強のバックアップ！）
        Contact.objects.create(
            name=user_name,
            email=user_email,
            phone=user_phone,
            car_model=car_model,
            car_color=car_color,
            message=user_message
        )

        # 1. 管理者（社長様）に届くメールの「本文」を綺麗に作る
        admin_body = f"""ホームページから新しいお問い合わせがありました。

【お名前】 {user_name}
【メールアドレス】 {user_email}
【電話番号】 {user_phone}
【車種名】 {car_model}
【年式 / 色】 {car_color}

【ご相談内容】
{user_message}
"""
        
        # 2. EmailMessageを使って、管理者へ送信（返信先マジック付き）
        admin_email = EmailMessage(
            subject=f"【HP問合せ】{user_name}様より",
            body=admin_body,
            from_email='info@explorer13.jp',
            to=['info@explorer13.jp'],
            reply_to=[user_email]
        )
        admin_email.send()

        # 3. お客様への自動返信メール
        if user_email:
            auto_reply_subject = '【自動返信】お問い合わせありがとうございます'
            auto_reply_message = f'''{user_name} 様\n\nこの度は、お問い合わせいただき誠にありがとうございます。\n以下の内容で承りました。担当者より改めてご連絡いたします。\n\n-----------------------------------------\n【お問い合わせ内容】\n{user_message}\n-----------------------------------------\n※このメールは自動送信システムから送信されています。\n'''
            
            send_mail(
                auto_reply_subject,
                auto_reply_message,
                'info@explorer13.jp',
                [user_email],
                fail_silently=False,
            )

        return render(request, 'contact.html', {'success': True, 'setting': setting})
    
    return render(request, 'contact.html', {'setting': setting})

class CompanyView(TemplateView):
    template_name = 'company.html'

# --- 2. 裏側の管理ページ（操作する画面） ---

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = '/admin/login/'

def post_create(request):
    if request.method == 'POST':
        Post.objects.create(
            title=request.POST.get('title'),
            category=request.POST.get('category'),
            content=request.POST.get('content'),
            tag=request.POST.get('tag'),
            status=request.POST.get('status'),
            thumbnail=request.FILES.get('thumbnail'),
            image=request.FILES.get('image')
        )
        return redirect('dashboard')
    return render(request, 'post_edit.html', {'post': None})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.category = request.POST.get('category')
        post.content = request.POST.get('content')
        post.tag = request.POST.get('tag')
        post.status = request.POST.get('status')
        
        if request.FILES.get('thumbnail'):
            post.thumbnail = request.FILES.get('thumbnail')
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')
            
        post.save()
        return redirect('dashboard')
    return render(request, 'post_edit.html', {'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('dashboard')


# --- 3. データの受け渡し用（API） ---

def api_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    data = []
    for post in posts:
        if post.thumbnail:
            display_img = post.thumbnail.url
        elif post.image and not (".mp4" in post.image.url.lower() or ".mov" in post.image.url.lower()):
            display_img = post.image.url
        else:
            display_img = ''

        data.append({
            'id': post.id,
            'title': post.title,
            'category': post.category,
            'status': post.status,
            'date': post.created_at.strftime('%Y-%m-%d'),
            'image': display_img,
        })
    return JsonResponse({'posts': data})

def api_post_delete(request, pk):
    if request.method == 'POST':
        try:
            post = Post.objects.get(pk=pk)
            post.delete()
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})

def test_design(request):
    return render(request, 'index_test.html')