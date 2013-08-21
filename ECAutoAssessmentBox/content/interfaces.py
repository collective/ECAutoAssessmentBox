# -*- coding: utf-8 -*-
# $Id: interfaces.py 1584 2011-08-14 09:45:05Z amelung $
#
# Copyright (c) 2006-2011 Otto-von-Guericke-UniversitŠt Magdeburg
#
# This file is part of ECAutoAssessmentBox.
#
__author__ = """Mario Amelung <mario.amelung@gmx.de>"""
__docformat__ = 'plaintext'

from zope.interface import Interface

class IECAutoAssessmentBox(Interface):
    """Marker interface for .ECAutoAssessmentBox.ECAutoAssessmentBox
    """

class IECAutoAssignment(Interface):
    """Marker interface for .ECAutoAssignment.ECAutoAssignment
    """
