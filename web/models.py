from django.db import models
from django.utils import timezone # 🌟 新しく追加（Contactモデルの日時記録用）

# --- 既存のPostモデル（そのままです） ---
class Post(models.Model):
    CATEGORY_CHOICES = [
        ('Blog', 'Blog'),
        ('Works', 'Works'),
    ]
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Blog')
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    image = models.FileField(upload_to='post_images/', null=True, blank=True)
    tag = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Published')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# --- 🌟 新規追加：お問い合わせ保存用のモデル（データベースの箱） ---
class Contact(models.Model):
    name = models.CharField('お名前', max_length=100)
    email = models.EmailField('メールアドレス')
    phone = models.CharField('電話番号', max_length=20) # 必須設定
    car_model = models.CharField('車種名', max_length=100)
    car_color = models.CharField('年式/色', max_length=100, blank=True, null=True)
    message = models.TextField('ご相談内容')
    created_at = models.DateTimeField('送信日時', default=timezone.now)

    def __str__(self):
        return f"{self.name}様からの問い合わせ ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = 'お問い合わせ'
        verbose_name_plural = 'お問い合わせ一覧'