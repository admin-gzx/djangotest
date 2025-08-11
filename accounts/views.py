# 导入Django的render函数，用于渲染模板
from django.shortcuts import render
# 导入redirect函数，用于重定向
from django.shortcuts import redirect
# 导入用户认证相关函数
from django.contrib.auth import authenticate, login, logout
# 导入登录装饰器
from django.contrib.auth.decorators import login_required
# 导入消息提示函数
from django.contrib import messages
# 导入自定义表单
from .forms import RegisterForm, LoginForm


def register(request):
    """用户注册视图

    处理新用户的注册请求

    参数:
        request: HTTP请求对象

    返回:
        渲染后的注册页面或重定向到登录页面
    """
    # 如果用户已登录，重定向到主页
    if request.user.is_authenticated:
        return redirect('home')

    # 处理POST请求
    if request.method == 'POST':
        # 绑定表单数据
        form = RegisterForm(request.POST)
        # 验证表单数据
        if form.is_valid():
            # 保存用户数据
            form.save()
            # 获取用户名
            username = form.cleaned_data.get('username')
            # 显示成功消息
            messages.success(request, f'账号创建成功！你现在可以登录了，{username}！')
            # 重定向到登录页面
            return redirect('login')
    # 处理GET请求
    else:
        # 初始化表单
        form = RegisterForm()

    # 渲染模板并返回响应
    return render(request, 'accounts/accounts_register.html', {'form': form})


def login_view(request):
    """用户登录视图

    处理用户的登录请求

    参数:
        request: HTTP请求对象

    返回:
        渲染后的登录页面或重定向到主页/指定页面
    """
    # 如果用户已登录，重定向到主页
    if request.user.is_authenticated:
        return redirect('home')

    # 处理POST请求
    if request.method == 'POST':
        # 绑定表单数据
        form = LoginForm(request.POST)
        # 验证表单数据
        if form.is_valid():
            # 获取用户名和密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 验证用户身份
            user = authenticate(request, username=username, password=password)

            # 如果验证成功
            if user is not None:
                # 登录用户
                login(request, user)
                # 检查是否有next参数
                next_page = request.GET.get('next')
                # 如果有next参数，跳转到指定页面，否则跳转到主页
                return redirect(next_page) if next_page else redirect('home')
            # 验证失败
            else:
                messages.error(request, '用户名或密码不正确')
    # 处理GET请求
    else:
        # 初始化表单
        form = LoginForm()

    # 渲染模板并返回响应
    return render(request, 'accounts/accounts_login.html', {'form': form})


def logout_view(request):
    """用户注销视图

    处理用户的注销请求

    参数:
        request: HTTP请求对象

    返回:
        重定向到登录页面
    """
    # 注销用户
    logout(request)
    # 显示信息消息
    messages.info(request, '你已成功注销')
    # 重定向到登录页面
    return redirect('login')



