from django.db import models

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