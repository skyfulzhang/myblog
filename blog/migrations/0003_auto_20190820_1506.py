# Generated by Django 2.2.3 on 2019-08-20 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190820_1210'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogarticle',
            options={'ordering': ['-created_time'], 'verbose_name': '博客文章', 'verbose_name_plural': '博客文章'},
        ),
        migrations.AlterModelOptions(
            name='blogcategory',
            options={'ordering': ['-created_time'], 'verbose_name': '博客分类', 'verbose_name_plural': '博客分类'},
        ),
        migrations.AlterModelOptions(
            name='blogtag',
            options={'ordering': ['-created_time'], 'verbose_name': '博客标签', 'verbose_name_plural': '博客标签'},
        ),
    ]
