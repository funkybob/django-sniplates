import os

from django.template import Context


HERE = os.path.dirname(__file__)


def template_path(path):
    return os.path.join(HERE, 'templates', path, '')


class TemplateTestMixin(object):

    def setUp(self):
        self.ctx = Context()

    def assertNotInHTML(self, needle, haystack, msg_prefix=''):
        self.assertInHTML(needle, haystack, count=0, msg_prefix=msg_prefix)
