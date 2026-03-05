from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

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
            # ▼ ここが最終修正版の動画タグです（preload="auto" などを追加） ▼
            video_tag = f'<video src="{post.image.url}" class="video-player" controls preload="auto" playsinline></video>'
            
            if "[video]" in post.content:
                post.content = post.content.replace("[video]", video_tag)
            else:
                # [video] タグがない場合は、一番下に自動で追加
                post.content += f"<br><br>{video_tag}"
        
        context['post'] = post
        return context

def contact(request):
    if request.method == 'POST':
        send_mail(
            f"問い合わせ: {request.POST.get('name')}",
            request.POST.get('message'),
            'ysproject56722020@gmail.com',
            ['ysproject56722020@gmail.com']
        )

# --- ここから追加：お客様への自動返信メール ---
        user_name = request.POST.get('name')
        user_email = request.POST.get('email')
        user_message = request.POST.get('message')

        if user_email:  # 念のため、メールアドレスが入力されているか確認
            auto_reply_subject = '【自動返信】お問い合わせありがとうございます'
            auto_reply_message = f'''{user_name} 様

この度は、お問い合わせいただき誠にありがとうございます。
以下の内容で承りました。担当者より改めてご連絡いたします。

-----------------------------------------
【お問い合わせ内容】
{user_message}
-----------------------------------------
※このメールは自動送信システムから送信されています。
'''
        send_mail(
            auto_reply_subject,
            auto_reply_message,
            'ysproject56722020@gmail.com',  # 今の送信元（本番時に info@... に変更）
            [user_email],  # お客様のメールアドレス宛
            fail_silently=False,
            )
        # --- ここまで追加 ---

        return render(request, 'contact.html', {'success': True})
    return render(request, 'contact.html')

class CompanyView(TemplateView):
    template_name = 'company.html'


# --- 2. 裏側の管理ページ（大久保様が操作する画面） ---

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
            thumbnail=request.FILES.get('thumbnail'), # サムネイル画像
            image=request.FILES.get('image')           # メインメディア（画像/動画）
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
        # 管理画面の一覧で表示する画像を選択
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