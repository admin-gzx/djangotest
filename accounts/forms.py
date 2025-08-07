from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """用户注册表单，继承自Django内置的UserCreationForm"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})  # 添加样式
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),  # 用户名样式
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),  # 密码1样式
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),  # 密码2样式
        }

    def save(self, commit=True):
        """保存用户信息，包括邮箱"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """用户登录表单"""
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )