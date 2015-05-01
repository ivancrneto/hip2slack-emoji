# coding: utf-8
from setuptools import setup
from setuptools.command.test import test as TestCommand
import codecs
import io
import os
import sys

import hip2slack_emoji

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()

long_description = read('README.rst')
requirements = read('requirements.txt')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='hip2slack-emoji',
    version=hip2slack_emoji.__version__,
    url='http://github.com/ivancrneto/hip2slack-emoji/',
    license='MIT License',
    author='Ivan Rocha',
    tests_require=['pytest'],
    install_requires=requirements,
    cmdclass={'test': PyTest},
    author_email='ivan.cr.neto@gmail.com',
    description='Importer of Hipchat emojis to Slack',
    long_description=long_description,
    packages=['hip2slack_emoji'],
    entry_points={
	'console_scripts': ['catchemall=hip2slack_emoji.problem:main']
    },
    include_package_data=True,
    package_data = {
        '': ['requirements.txt'],
    },
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    extras_require={
        'testing': ['pytest'],
    }
)
