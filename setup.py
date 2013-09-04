#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    'sentry>=6.0.0',
    'lighthouse>=0.1',
]

f = open('README.rst')
readme = f.read()
f.close()

setup(
    name='sentry_lighthouse',
    version='0.1.1',
    author='Gunnlaugur Thor Briem',
    author_email='gunnlaugur@gmail.com',
    url='http://github.com/gthb/sentry-lighthouse',
    description='A Sentry extension which creates Lighthouse issues from sentry events.',
    long_description=readme,
    license='BSD',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'sentry.apps': [
            'sentry_lighthouse = sentry_lighthouse',
        ],
        'sentry.plugins': [
            'sentry_lighthouse = sentry_lighthouse.plugin:LighthousePlugin'
        ],
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Software Development'
    ],
)
