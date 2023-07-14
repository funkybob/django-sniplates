import copy
import os

from django.conf import settings
from django.test import override_settings

HERE = os.path.dirname(__file__)


def template_path(path):
    return os.path.join(HERE, 'templates', path, '')


def template_dirs(*relative_dirs):
    """
    Convenient decorator to specify the template path.
    """
    # copy the original setting
    TEMPLATES = copy.deepcopy(settings.TEMPLATES)
    for tpl_cfg in TEMPLATES:
        tpl_cfg['DIRS'] = [template_path(rel_dir) for rel_dir in relative_dirs]
    return override_settings(TEMPLATES=TEMPLATES)


class TemplateTestMixin(object):

    def setUp(self):
        self.ctx = {}

    def assertNotInHTML(self, needle, haystack, msg_prefix=''):
        self.assertInHTML(needle, haystack, count=0, msg_prefix=msg_prefix)
