from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-+l&i-!je5oxbg4f8zl0i90+v!3tn#83=a_hs+(6iav#7a-96$r'

DEBUG = True

# Lista de hosts permitidos para o aplicativo, incluindo localhost e ngrok.
ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    '.ngrok-free.app'
]

# Lista de origens confiáveis para proteção contra CSRF, permitindo acesso de ngrok.
CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.app'
]

CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Define a configuração de URLs raiz do projeto e as opções para o sistema de templates do Django.
ROOT_URLCONF = 'urban_farm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', # Backend de templates do Django
        'DIRS': [], # Diretórios adicionais para buscar templates (vazio neste caso)
        'APP_DIRS': True, # Permite que o Django busque templates em diretórios de aplicativos
        'OPTIONS': {     
            'context_processors': [  # Processadores de contexto para adicionar variáveis ao contexto dos templates
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'urban_farm.wsgi.application'
# Configuração do banco de dados para o Django, utilizando SQL Server com ODBC.
DATABASES = {
    'default': {
        'ENGINE': 'mssql',  # Motor do banco de dados (SQL Server)
        'NAME': 'urban_farm',  # Nome do banco de dados
        'USER': 'sa',  # Nome do usuário para autenticação
        'PASSWORD': '4268',  # Senha do usuário
        'HOST': 'DESKTOP-LISMFBG',  # Host onde o banco de dados está localizado
        'PORT': '',  # Porta do banco de dados (vazia para padrão)
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',  # Driver ODBC utilizado para conexão
        },
    }
}

# Configuração dos validadores de senha para o sistema de autenticação do Django.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Configuração do URL base para arquivos estáticos (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Caminhos adicionais onde o Django deve procurar arquivos estáticos no 'core'
STATICFILES_DIRS = [
    BASE_DIR / "core/static",
]

# Caminho para onde o comando 'collectstatic' colocará todos os arquivos
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
