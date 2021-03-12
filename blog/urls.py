from django.urls import path, include, re_path
from blog import views

urlpatterns = [
    path('index/', views.home, name='index'),
    path('article-list/', views.article_list, name='article_list'),
    path('article-hot/', views.article_hot, name='article_hot'),
    path('article-django/', views.article_django, name='article_django'),
    path('article-flask/', views.article_flask, name='article_flask'),
    path('article-scrapy/', views.article_scrapy, name='article_scrapy'),
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    path('article-comment/<int:id>/', views.article_comment, name='article_comment'),
]
