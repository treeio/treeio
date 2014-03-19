from django.test.simple import DjangoTestSuiteRunner
from django.conf import settings


class CustomTestRunner(DjangoTestSuiteRunner):

    """Custom DjangoTestSuiteRunner to remove Django modules from tests"""

    def __init__(self, *args, **kwargs):
        super(CustomTestRunner, self).__init__(*args, **kwargs)

    def run_tests(self, test_labels, **kwargs):
        test_labels = [app[7:]
                       for app in settings.INSTALLED_APPS if 'treeio' in app and app.count('.') == 1]
        return super(CustomTestRunner, self).run_tests(test_labels, **kwargs)
