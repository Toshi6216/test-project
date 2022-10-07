from django.db import models

class NippoModel(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class ContentsCard(models.Model):
    subtitle = models.CharField(max_length=100)
    content = models.TextField()
    post = models.ForeignKey(
        Post,
        related_name = "contentscard",
        on_delete = models.CASCADE
    )

    def __str__(self):
        return self.subtitle