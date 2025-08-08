from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm


def register(request):
    """用户注册视图"""
    # 如果用户已登录，重定向到主页
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'账号创建成功！你现在可以登录了，{username}！')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/accounts_register.html', {'form': form})


def login_view(request):
    """用户登录视图"""
    # 如果用户已登录，重定向到主页
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # 如果有next参数，跳转到指定页面，否则跳转到主页
                next_page = request.GET.get('next')
                return redirect(next_page) if next_page else redirect('home')
            else:
                messages.error(request, '用户名或密码不正确')
    else:
        form = LoginForm()
    return render(request, 'accounts/accounts_login.html', {'form': form})


def logout_view(request):
    """用户注销视图"""
    logout(request)
    messages.info(request, '你已成功注销')
    return redirect('login')



