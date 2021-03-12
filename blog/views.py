from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from blog import models
import markdown
# 引入分页模块
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.
def home(request):
    return render(request, "blog/index.html")


# 文章列表
@login_required(login_url='/userinfo/login/')
def article_list(request):
    search = request.GET.get('search')
    if search:
        search = search
        article_list = models.BlogArticle.objects.filter(
            Q(name__icontains=search) |
            Q(summary__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ""
        article_list = models.BlogArticle.objects.all()
    # 每页显示 5 篇文章
    paginator = Paginator(article_list, 5)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    return render(request, "blog/article_list.html", context={"articles": articles, "search": search})


# 热门文章
@login_required(login_url='/userinfo/login/')
def article_hot(request):
    search = request.GET.get('search')
    if search:
        search = search
        article_list = models.BlogArticle.objects.filter(
            Q(name__icontains=search) |
            Q(summary__icontains=search) |
            Q(body__icontains=search)
        ).order_by("-total_views")
    else:
        search = ""
        article_list = models.BlogArticle.objects.all().order_by("-total_views")
    # 每页显示 1 篇文章
    paginator = Paginator(article_list, 5)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    return render(request, "blog/article_list.html", context={"articles": articles, "search": search})


def article_django(request):
    category = models.BlogCategory.objects.get(title="Django 学习")
    article_list = category.article_category.all()
    paginator = Paginator(article_list, 5)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, "blog/article_list.html", context={"articles": articles})


def article_flask(request):
    category = models.BlogCategory.objects.get(title="Flask 学习")
    article_list = category.article_category.all()
    paginator = Paginator(article_list, 5)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, "blog/article_list.html", context={"articles": articles})


def article_scrapy(request):
    category = models.BlogCategory.objects.get(title="Scrapy 爬虫")
    article_list = category.article_category.all()
    paginator = Paginator(article_list, 5)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, "blog/article_list.html", context={"articles": articles})


# 文章详情
def article_detail(request, id):
    article = get_object_or_404(models.BlogArticle, id=id)
    try:
        # 过滤出所有的id比当前文章小的文章
        pre_articles = models.BlogArticle.objects.filter(id__lt=article.id).order_by('-id')
        # 过滤出id大的文章
        next_articles = models.BlogArticle.objects.filter(id__gt=article.id).order_by('id')
    except Exception as e:
        pass
    else:
        # 取出相邻前一篇文章
        if pre_articles.count() > 0:
            pre_article = pre_articles[0]
        else:
            pre_article = None
        # 取出相邻后一篇文章
        if next_articles.count() > 0:
            next_article = next_articles[0]
        else:
            next_article = None
        # 引入评论表单
        comment_form = BlogCommentForm()
        # 取出文章评论
        comments = models.BlogComment.objects.filter(article=id)
        # 阅读加1
        article.total_views += 1
        article.save(update_fields=['total_views'])
        # 将markdown语法渲染成html样式
        article.body = markdown.markdown(article.body,
                                         extensions=[
                                             # 包含 缩写、表格等常用扩展
                                             'markdown.extensions.extra',
                                             # 语法高亮扩展
                                             'markdown.extensions.codehilite',
                                             # 目录扩展
                                             'markdown.extensions.toc',
                                         ])
        context = {"article": article, 'comments': comments, 'comment_form': comment_form, 'pre_article': pre_article,
                   'next_article': next_article, }
        return render(request, "blog/article_detail.html", context=context)


# 引入表单类
from django import forms


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = models.BlogComment
        fields = ['body', ]


# 文章评论
def article_comment(request, id):
    article = get_object_or_404(models.BlogArticle, id=id)
    if request.method == 'POST':
        comment_form = BlogCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            return redirect(reverse("blog:article_detail", args=[id, ]))
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        return HttpResponse("发表评论仅接受POST请求。")
