from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from userinfo import models


# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = models.UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("blog:index")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        user_register_form = models.UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userinfo/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        user_login_form = models.UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("blog:index")
            else:
                return HttpResponse("账号或密码输入有误。请重新输入~")
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == 'GET':
        user_login_form = models.UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userinfo/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


# 用户退出
def user_logout(request):
    logout(request)
    return redirect("blog:index")


@login_required(login_url='/userinfo/login/')
def user_delete(request, id):
    user = User.objects.get(id=id)
    # 验证登录用户、待删除用户是否相同
    if request.user == user:
        # 退出登录，删除数据并返回博客列表
        logout(request)
        user.delete()
        return redirect("blog:index")
    else:
        return HttpResponse("你没有删除操作的权限。")


@login_required(login_url='/userinfo/login/')
def user_update(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段
    userinfo = models.UserInfo.objects.get(user_id=id)
    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")
        data_form = models.UserInfoForm(request.POST, )
        print(data_form)
        print("*" * 100)
        print(request.FILES, request.FILES['avatar'])
        if data_form.is_valid():
            # 取得清洗后的合法数据
            verified_data = data_form.cleaned_data
            print(verified_data)
            userinfo.phone = verified_data['phone']
            userinfo.city = verified_data['city']
            userinfo.profile = verified_data['profile']
            if 'avatar' in request.FILES:
                userinfo.avatar = request.FILES["avatar"]
            userinfo.save()
            # 带参数的 redirect()
            return redirect("blog:index")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")

    elif request.method == 'GET':
        user_form = models.UserInfoForm()
        context = {'user_form': user_form, 'userinfo': userinfo, 'user': user}
        return render(request, 'userinfo/update.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")
