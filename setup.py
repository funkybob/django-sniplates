from setuptools import setup, find_packages

setup(
    name='django-sniplates',
    version='0.7.0',
    description='Efficient template macro sets for Django',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='http://github.com/funkybob/django-sniplates',
    keywords=['django', 'templates', 'forms'],
    packages=find_packages(exclude=('tests*',)),
    include_package_data=True,
    zip_safe=False,
    # tests
    test_suite='runtests.runtests',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    requires=[
        'Django (>=2.2)',
    ],
    install_requires=[
        'Django>=2.2',
    ],
)
