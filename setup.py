from setuptools import setup, find_packages

setup(
    name='django-sniplates',
    version='0.1.0',
    description='Efficient template macro sets for Django',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='http://github.com/funkybob/django-sniplates',
    keywords=['django', 'templates',],
    packages = find_packages(exclude=('tests*',)),
    zip_safe=False,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    requires = [
        'Django (>=1.7)',
    ],
    install_requires = [
        'Django>=1.7',
    ],
)
