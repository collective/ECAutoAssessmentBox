# -*- coding: utf-8 -*-
#
# $Id$

import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = read('Products', 'ECAutoAssessmentBox', 'version.txt').strip()
readme  = read('Products', 'ECAutoAssessmentBox', 'README.txt')
history = read('Products', 'ECAutoAssessmentBox', 'CHANGES.txt')

long_description = readme + '\n\n' + history

setup(name='Products.ECAutoAssessmentBox',
      version=version,
      description = "Submissions for programming assignments with immediate feedback from ECSpooler.",
      long_description = long_description,

      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords = '',
      author = 'Mario Amelung',
      author_email = 'mario.amelung@gmx.de',
      url = 'http://plone.org/products/ecautoassessmentbox/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Products.ECAssignmentBox >= 1.4',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
