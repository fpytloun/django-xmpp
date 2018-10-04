#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()

setup(
    name='django-xmpp',
    version='0.4',
    description='XMPP integration for Django app made simple',
    long_description=readme,
    author="Filip Pytloun",
    author_email='filip@pytloun.cz',
    url='https://github.com/fpytloun/django-xmpp',
    license='GPLv2',
    packages=['xmpp', 'xmpp.templatetags', 'xmpp.management',
              'xmpp.management.commands'],
    include_package_data=True,
    install_requires=['django', 'sleekxmpp', 'dnspython', 'pyasn1',
                      'pyasn1_modules', 'django-gravatar2'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='django xmpp conversejs jabber chat ejabberd',
)
