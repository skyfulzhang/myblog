from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.
# 博客分类
from django.urls import reverse


class BlogCategory(models.Model):
    title = models.CharField(max_length=64, verbose_name="博客分类")
    created_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    modified_time = models.DateTimeField(auto_now_add=True, verbose_name="最后修改时间")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blog_category'
        ordering = ["-created_time"]
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name


# 博客标签
class BlogTag(models.Model):
    title = models.CharField(max_length=64, verbose_name="博客标签")
    created_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    modified_time = models.DateTimeField(auto_now_add=True, verbose_name="最后修改时间")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blog_tag'
        ordering = ["-created_time"]
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name


"""
图片上传可以使用第三方库：django-imagekit，
实例： 
# 引入imagekit
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
class ArticlePost(models.Model):
    ...
    avatar = ProcessedImageField(
        upload_to='picture/%Y%m%d',#上传位置
        processors=[ResizeToFit(width=400)],#处理规则
        format='JPEG', #存储格式
        options={'quality': 100}, #图片质量
    )
    
当存在外键时，直接使用 related_name使用，不纠结！


"""


# 博客文章
class BlogArticle(models.Model):
    name = models.CharField(max_length=128, verbose_name="博客标题")
    picture = models.ImageField(upload_to='blog/', blank=True)
    body = RichTextField(config_name="default", verbose_name="博客内容")
    author = models.ForeignKey(User, verbose_name="博客作者", on_delete=models.CASCADE)
    summary = models.CharField(max_length=256, blank=True, verbose_name="博客摘要")
    category = models.ForeignKey(BlogCategory, verbose_name="博客分类", on_delete=models.CASCADE,
                                 related_name="article_category")
    tags = models.ManyToManyField(BlogTag, blank=True, verbose_name="博客标签")
    total_views = models.PositiveIntegerField(default=0, verbose_name="浏览量")
    created_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    modified_time = models.DateTimeField(auto_now_add=True, verbose_name="最后修改时间")

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[self.id])

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'blog_article'
        ordering = ["-created_time"]
        verbose_name = '博客文章'
        verbose_name_plural = verbose_name


# 博客评论
class BlogComment(models.Model):
    article = models.ForeignKey(BlogArticle, on_delete=models.CASCADE, related_name='comments', verbose_name="博客标题")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="博客作者")
    body = RichTextField(config_name="default", verbose_name="博客评论")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")

    def __str__(self):
        return self.body

    class Meta:
        db_table = 'blog_comment'
        ordering = ["-created_time"]
        verbose_name = '博客评论'
        verbose_name_plural = verbose_name
