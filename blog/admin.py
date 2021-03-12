from django.contrib import admin
from blog import models


# Register your models here.

# Register your models here.
class BlogCategoryAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('title', 'modified_time')
    # 筛选
    list_filter = ('title',)
    # 每页记录数
    list_per_page = 25
    # 查询字段
    search_fields = ('title',)


class BlogTagAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('title', 'modified_time')
    # 筛选
    list_filter = ('title',)
    # 每页记录数
    list_per_page = 25
    # 查询字段
    search_fields = ('title',)


class BlogArticleAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('name', 'author', 'summary', 'category', 'tag_list', 'modified_time')
    # 筛选
    list_filter = ('name', 'author', 'summary', 'category',)
    # 每页记录数
    list_per_page = 25
    # 查询字段
    search_fields = ('name', 'author', 'summary', 'category')
    # # 只针对多对多
    filter_horizontal = ('tags',)
    # # 只针对外键的
    raw_id_fields = ('category',)

    # list_display处理多对多
    def tag_list(self, obj):
        return [tag.title for tag in obj.tags.all()]

    tag_list.short_description = "博客标签"


class BlogCommentAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('article', 'user', 'body', 'created_time')
    # 筛选
    list_filter = ('article', 'user',)
    # 每页记录数
    list_per_page = 25
    # 查询字段
    search_fields = ('article', 'user',)


admin.site.register(models.BlogCategory, BlogCategoryAdmin)
admin.site.register(models.BlogTag, BlogTagAdmin)
admin.site.register(models.BlogArticle, BlogArticleAdmin)
admin.site.register(models.BlogComment, BlogCommentAdmin)
