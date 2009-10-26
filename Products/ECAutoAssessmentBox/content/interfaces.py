# -*- coding: utf-8 -*-
# $Id$
#
# Copyright (c) 2006-2009 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECAutoAssessmentBox.
#
__author__ = """Mario Amelung <mario.amelung@gmx.de>"""
__docformat__ = 'plaintext'
__version__   = '$Revision$'

from zope.interface import Interface

class IECAutoAssessmentBox(Interface):
    """Marker interface for .ECAutoAssessmentBox.ECAutoAssessmentBox
    """

class IECAutoAssignment(Interface):
    """Marker interface for .ECAutoAssignment.ECAutoAssignment
    """
