import os

from django.template import Context
try:
    from django.test import override_settings
except ImportErrror:  # 1.4 Compatibility
    from django.test.utils import override_settings

HERE = os.path.dirname(__file__)


def template_path(path):
    return os.path.join(HERE, 'templates', path, '')


class TemplateTestMixin(object):

    def setUp(self):
        self.ctx = Context()
