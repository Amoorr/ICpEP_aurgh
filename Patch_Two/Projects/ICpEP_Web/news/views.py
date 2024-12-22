from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib import messages
from django.db.models import Q
from .models import NewsArticle, ArticlePhoto, NewsView
from .forms import NewsArticleForm, ArticlePhotoForm
from accounts.decorators import role_required
from django.shortcuts import render

# List news articles with search functionality
@login_required
def student_news_list(request):
    query = request.GET.get('search', '')  # Get search query from GET request
    # Filter news articles based on search query (title contains the search term)
    news_list = NewsArticle.objects.filter(title__icontains=query).order_by('-publication_date')
    
    return render(request, 'news/student/student_news_list.html', {
        'news_list': news_list,
    })

# View a specific news article with its details (title, content, author, images)
@login_required
def student_news_detail(request, article_id):
    news_article = get_object_or_404(NewsArticle, pk=article_id)
    
    # Track the view count for the student
    student = request.user  # The logged-in user is a CustomUser
    view_record, created = NewsView.objects.get_or_create(student=student, article=news_article)

    # If a new view record is created, increment the view count for the article
    if created:
        news_article.view_count += 1
        news_article.save()

    # Get associated photos for the article
    photos = ArticlePhoto.objects.filter(article=news_article)

    return render(request, 'news/student/student_news_detail.html', {
        'news_article': news_article,
        'photos': photos,
    })

@login_required
@role_required('admin')
def admin_news(request):
    query = request.GET.get('search', '')
    # Filter articles by title or content if search query is provided
    news_list = NewsArticle.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    ) if query else NewsArticle.objects.all()
    
    return render(request, 'news/admin/admin_news.html', {'news_list': news_list})

@role_required('admin')
@login_required
def admin_add_news(request):
    # Define the formset for ArticlePhoto
    ArticlePhotoFormSet = modelformset_factory(ArticlePhoto, form=ArticlePhotoForm, extra=1)

    if request.method == 'POST':
        news_form = NewsArticleForm(request.POST)
        photo_formset = ArticlePhotoFormSet(request.POST, request.FILES)

        if news_form.is_valid() and photo_formset.is_valid() and any(form.cleaned_data for form in photo_formset):
            # Save the news article first
            news_article = news_form.save()

            # Save each photo in the formset
            for photo_form in photo_formset:
                if photo_form.cleaned_data:
                    photo = photo_form.save(commit=False)
                    photo.article = news_article  # Associate the photo with the news article
                    photo.save()

            messages.success(request, "News article added successfully!")
            return redirect('news:admin_news')
        else:
            messages.error(request, "Please fix the errors below.")
            print("News Form Errors:", news_form.errors)
            print("Photo Formset Errors:", photo_formset.errors)
    else:
        news_form = NewsArticleForm()
        photo_formset = ArticlePhotoFormSet(queryset=ArticlePhoto.objects.none())

    return render(request, 'news/admin/admin_add_news.html', {
        'news_form': news_form,
        'photo_formset': photo_formset
    })

@login_required
@role_required('admin')
def admin_edit_news(request, article_id):
    # Get the news article object
    news = get_object_or_404(NewsArticle, pk=article_id)

    # Define the formset for ArticlePhoto
    ArticlePhotoFormSet = modelformset_factory(ArticlePhoto, form=ArticlePhotoForm, extra=1, can_delete=True)

    if request.method == 'POST':
        # Bind forms with submitted data
        news_form = NewsArticleForm(request.POST, instance=news)
        photo_formset = ArticlePhotoFormSet(request.POST, request.FILES, queryset=ArticlePhoto.objects.filter(article=news))

        if news_form.is_valid() and photo_formset.is_valid():
            # Save the news article
            news_article = news_form.save()

            # Save or delete photos
            for photo_form in photo_formset:
                if photo_form.cleaned_data.get('DELETE', False):
                    photo_form.instance.delete()
                elif photo_form.cleaned_data:  # Avoid saving invalid/empty forms
                    photo = photo_form.save(commit=False)
                    photo.article = news_article  # Link photo to the article
                    photo.save()

            messages.success(request, "News article updated successfully!")
            return redirect('news:admin_news')
        else:
            messages.error(request, "Please fix the errors below.")
            print("News Form Errors:", news_form.errors)
            print("Photo Formset Errors:", photo_formset.errors)
    else:
        # Populate the forms with existing data
        news_form = NewsArticleForm(instance=news)
        photo_formset = ArticlePhotoFormSet(queryset=ArticlePhoto.objects.filter(article=news))

    return render(request, 'news/admin/admin_edit_news.html', {
        'news_form': news_form,
        'photo_formset': photo_formset
    })

@login_required
@role_required('admin')
def admin_delete_news(request, article_id):
    news = get_object_or_404(NewsArticle, pk=article_id)
    if request.method == 'POST':
        news.delete()
        messages.success(request, "News article deleted successfully!")
        return redirect('news:admin_news')
    
    return render(request, 'news/admin/admin_delete_news.html', {'news': news})
