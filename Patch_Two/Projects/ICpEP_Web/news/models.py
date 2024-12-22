from django.db import models
from accounts.models import CustomUser

class NewsArticle(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=0)
    subhead = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'NewsArticles'  # Specify the table name if you need to override Django's default behavior


class ArticlePhoto(models.Model):
    photo_id = models.AutoField(primary_key=True)
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='photos')
    image_path = models.ImageField(upload_to='article_photos/', blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Photo for {self.article.title}"
    
    class Meta:
        db_table = 'ArticlePhotos'  # Specify the table name if you need to override Django's default behavior

class NewsView(models.Model):
    view_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'NewsViews'
        unique_together = ('student', 'article')

    def __str__(self):
        return f'{self.student.last_name} viewed {self.article.title}'


