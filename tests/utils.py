import django

from django.template import Context

if django.VERSION < (1, 8):
    from django.test.utils import setup_test_template_loader, restore_template_loaders

    class TemplateTestMixin(object):
        TEMPLATES = {}

        @classmethod
        def setUpClass(cls):
            setup_test_template_loader(cls.TEMPLATES)

        @classmethod
        def tearDownClass(cls):
            restore_template_loaders()

        def setUp(self):
            self.ctx = Context()
else:
    from django.test.utils import override_settings

    class TemplateTestMixin(object):
        TEMPLATES = {}

        @classmethod
        def setUpClass(cls):
            cls.override = override_settings(TEMPLATES=[{
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'OPTIONS': {
                    'loaders': [
                        ('django.template.loaders.locmem.Loader', cls.TEMPLATES),
                    ],
                },
            }])
            cls.override.enable()

        @classmethod
        def tearDownClass(cls):
            cls.override.disable()

        def setUp(self):
            self.ctx = Context()
