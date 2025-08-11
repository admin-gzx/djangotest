import os
from pathlib import Path

# 项目根目录
# 使用Path对象获取当前文件的父级目录的父级目录，即项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全密钥，用于加密会话数据、密码重置令牌等
# 生产环境应使用环境变量存储，例如: os.environ.get('SECRET_KEY')
SECRET_KEY = 'django-insecure-your-secret-key-here'

# 调试模式
# 开发环境设为True，生产环境必须设为False
DEBUG = True

# 允许访问的主机列表
# 生产环境应添加实际域名，例如: ['example.com', 'www.example.com']
ALLOWED_HOSTS = []

# 应用配置
# 列出项目中安装的所有应用
INSTALLED_APPS = [
    'django.contrib.admin',  # Django后台管理系统
    'django.contrib.auth',   # Django认证系统
    'django.contrib.contenttypes',  # 内容类型框架，用于跟踪模型与权限
    'django.contrib.sessions',   # 会话管理，处理用户会话
    'django.contrib.messages',   # 消息框架，用于显示一次性通知
    'django.contrib.staticfiles',  # 静态文件管理，处理CSS、JS等
    # 自定义应用
    'accounts',  # 用户账户管理应用
    'products',  # 商品管理应用
    'carts',     # 购物车管理应用
    'orders',    # 订单管理应用
]

# 中间件配置
# 处理请求和响应的中间件列表，按照顺序执行
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # 安全相关中间件
    'django.contrib.sessions.middleware.SessionMiddleware',  # 会话管理中间件
    'django.middleware.common.CommonMiddleware',  # 处理常见请求/响应
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF保护中间件
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 认证中间件
    'django.contrib.messages.middleware.MessageMiddleware',  # 消息中间件
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 防点击劫持中间件
]

# 主URL配置
# 指定项目的根URL配置模块
ROOT_URLCONF = 'user_auth_system.urls'

# 媒体文件配置
# 媒体文件URL前缀
MEDIA_URL = '/media/'
# 媒体文件存储路径
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 全局模板目录
        'APP_DIRS': True,  # 是否在应用目录中查找模板
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # 调试上下文
                'django.template.context_processors.request',  # 请求对象
                'django.contrib.auth.context_processors.auth',  # 用户认证
                'django.contrib.messages.context_processors.messages',  # 消息
                'carts.context_processors.cart_item_count',  # 购物车数量处理器
                'products.context_processors.categories',  # 商品分类处理器
            ],
        },
    },
]

# WSGI应用
# 指定WSGI应用对象
WSGI_APPLICATION = 'user_auth_system.wsgi.application'

# 数据库配置 - MySQL
# 生产环境应使用环境变量存储敏感信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'django_taoduoduo',  # 数据库名，需要先在MySQL中创建
        'USER': 'root',         # 数据库用户名
        'PASSWORD': '123456',  # 数据库密码
        'HOST': 'localhost',    # 数据库主机
        'PORT': '3306',         # 数据库端口
    }
}

# 密码验证规则
# 定义用户密码的验证规则
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {'user_attributes': ('username', 'email')}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 国际化配置
LANGUAGE_CODE = 'en-us'  # 语言代码，中文可设置为'zh-hans'
TIME_ZONE = 'UTC'  # 时区，中国可设置为'Asia/Shanghai'
USE_I18N = True  # 是否启用国际化
USE_TZ = True  # 是否使用时区

# 静态文件配置
STATIC_URL = 'static/'  # 静态文件URL前缀
# 生产环境应配置STATIC_ROOT并使用collectstatic命令收集静态文件
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 默认主键字段类型
# 使用BigAutoField作为默认主键，支持更大的数值范围
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 登录URL
# 当@login_required装饰器检测到用户未登录时，重定向到该URL
LOGIN_URL = 'login'

# 登录成功后重定向的URL
# LOGIN_REDIRECT_URL = 'home'

# 日志配置
# 生产环境应配置详细的日志记录
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }
