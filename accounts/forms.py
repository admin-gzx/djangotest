# 导入Django表单基类
from django import forms
# 导入Django内置的用户创建表单
from django.contrib.auth.forms import UserCreationForm
# 导入Django内置的用户模型
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """用户注册表单

    继承自Django内置的UserCreationForm，扩展添加了邮箱字段

    字段:
        username: 用户名
        email: 邮箱
        password1: 密码
        password2: 确认密码
    """
    # 邮箱字段，设置为必填
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})  # 添加Bootstrap表单控件样式
    )

    class Meta:
        # 关联的模型
        model = User
        # 表单包含的字段
        fields = ['username', 'email', 'password1', 'password2']
        # 字段的小部件设置
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),  # 用户名输入框样式
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),  # 密码输入框样式
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),  # 确认密码输入框样式
        }

    def save(self, commit=True):
        """保存用户信息，包括邮箱

        重写父类的save方法，以保存邮箱信息

        参数:
            commit: 是否立即保存到数据库

        返回:
            保存后的用户对象
        """
        # 调用父类的save方法，但不立即提交到数据库
        user = super().save(commit=False)
        # 设置邮箱
        user.email = self.cleaned_data['email']
        # 如果需要立即提交
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """用户登录表单

    用于用户登录验证的表单

    字段:
        username: 用户名
        password: 密码
    """
    # 用户名字段
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})  # 添加Bootstrap表单控件样式
    )
    # 密码字段
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})  # 添加Bootstrap表单控件样式
    )