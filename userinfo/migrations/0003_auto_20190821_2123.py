# Generated by Django 2.2.4 on 2019-08-21 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0002_auto_20190821_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='image/%Y%m%d/', verbose_name='头像'),
        ),
    ]
