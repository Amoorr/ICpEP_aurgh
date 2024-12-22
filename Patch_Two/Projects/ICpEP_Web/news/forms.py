from django import forms
from .models import NewsArticle, ArticlePhoto

class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['title', 'content', 'author', 'subhead']

class ArticlePhotoForm(forms.ModelForm):
    class Meta:
        model = ArticlePhoto
        fields = ['image_path', 'caption']
        widgets = {
            'image_path': forms.ClearableFileInput(attrs={'required': False}),  # Optional input
        }


