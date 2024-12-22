from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('admin/', views.admin_news, name='admin_news'),
    path('admin/add/', views.admin_add_news, name='admin_add_news'),
    path('admin/<int:article_id>/edit/', views.admin_edit_news, name='admin_edit_news'),
    path('admin/<int:article_id>/delete/', views.admin_delete_news, name='admin_delete_news'),
    path('list/', views.student_news_list, name='student_news_list'),
    path('detail/<int:article_id>/', views.student_news_detail, name='student_news_detail'),
]
