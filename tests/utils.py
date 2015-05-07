import os

from django.template import Context
try:
    from django.test import override_settings  # NOQA
except ImportError:  # 1.4 Compatibility
    # The django 1.4 override_settings does not play nicely with decorating classes.
    from django.test.utils import override_settings as override_settings_
    from functools import wraps

    class override_settings(override_settings_):
        def __call__(self, test_func):
            from django.test import SimpleTestCase
            if isinstance(test_func, type):
                if not issubclass(test_func, SimpleTestCase):
                    raise Exception("Only subclasses of SimpleTestCase can be decorated")

                def __call__(innerself, result=None):
                    self.enable()
                    super(test_func, innerself).__call__(result)
                    self.disable()

                test_func.__call__ = __call__
                return test_func
            else:
                @wraps(test_func)
                def inner(*args, **kwargs):
                    with self:
                        return test_func(*args, **kwargs)
            return inner


HERE = os.path.dirname(__file__)


def template_path(path):
    return os.path.join(HERE, 'templates', path, '')


class TemplateTestMixin(object):

    def setUp(self):
        self.ctx = Context()
