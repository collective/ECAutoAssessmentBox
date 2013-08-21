# -*- coding: utf-8 -*-
# $Id: vocabularies.py 1584 2011-08-14 09:45:05Z amelung $
#
# Copyright (c) 2006-2011 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECAutoAssessmentBox.
#
__author__ = """Mario Amelung <mario.amelung@gmx.de>"""
__docformat__ = 'plaintext'
__version__   = '$Revision:1311 $'

""" 
Vocabularies used by control panel or widget
"""

from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.app.component.hooks import getSite
from Products.ATContentTypes.interfaces import IFileContent, IImageContent
from Products.Archetypes.interfaces.base import IBaseFolder
from Products.CMFCore.utils import getToolByName

from Products.ECAutoAssessmentBox import ECMessageFactory as _
from Products.ECAutoAssessmentBox import config


class ECAABBackendsVocabulary(object):
    """
    Vocabulary factory for backends
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        portal = getSite()
        
        ecs_tool = getToolByName(portal, config.ECS_NAME)
        
        items = [SimpleTerm('test', 'test', u'Test')]
        return SimpleVocabulary(items)
        
ECAABBackendsVocabularyFactory = ECAABBackendsVocabulary()        