from django.db import models

# Create your models here.
# 引入表单类
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User

# 注册用户表单
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserRegisterForm(forms.ModelForm):
    # 复写 User 的密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")


# 登录表单，继承了 forms.Form 类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# # 用户扩展信息
class UserInfo(models.Model):
    # 与 User 模型构成一对一的关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userinfo', verbose_name="用户")
    # 电话号码字段
    phone = models.CharField(max_length=11, blank=True, verbose_name="电话")
    # 城市字段
    city = models.CharField(max_length=64, blank=True, verbose_name="城市")
    # 头像
    avatar = models.ImageField(upload_to='image/%Y%m%d/', blank=True, verbose_name="头像")
    # 个人简介
    profile = models.TextField(max_length=500, blank=True, verbose_name="简介")
    # 创建时间
    created_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'userinfo'
        ordering = ["-created_time"]
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


#
# 信号接收函数，每当新建 User 实例时自动调用
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)


# 信号接收函数，每当更新 User 实例时自动调用
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userinfo.save()


#
# 扩展用户
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('phone', 'city', 'avatar', 'profile')
