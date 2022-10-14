from django.db import models

#日報モデル
class NippoModel(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


#テスト用ブログモデル
class Post(models.Model):
    title = models.CharField('タイトル', max_length=100)
    
    def __str__(self):
        return self.title

#テスト用コンテンツカード（タイトルと本文のセット）
class ContentsCard(models.Model):
    subtitle = models.CharField('サブタイトル', max_length=100)
    content = models.TextField('本文')
    post = models.ForeignKey(
        Post, verbose_name = '紐づく記事',
        related_name = "contentscard",
        on_delete = models.CASCADE
    )
    image = models.ImageField(
        upload_to='images', 
        verbose_name='イメージ画像', 
        null=True,
        blank=True
    )

    def __str__(self):
        return self.subtitle