
from django.template import Context
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

