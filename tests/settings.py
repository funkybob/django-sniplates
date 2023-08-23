DATABASES={
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS=(
    'sniplates',
    'tests',
)

MIDDLEWARE_CLASSES=[]

TEMPLATES=[
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True
        }
    },
]

USE_TZ = True
