# -*- coding: utf-8 -*-
# $Id$
#
# Copyright (c) 2006-2008 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECAutoAssessmentBox.
#
# ECAutoAssessmentBox is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# ECAutoAssessmentBox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ECAutoAssessmentBox; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
__author__ = """Mario Amelung <amelung@iws.cs.uni-magdeburg.de>"""
__docformat__ = 'plaintext'

from zope.interface import Interface

##code-section HEAD
##/code-section HEAD

class IECAutoAssessmentBox(Interface):
    """Marker interface for .ECAutoAssessmentBox.ECAutoAssessmentBox
    """

class IECAutoAssignment(Interface):
    """Marker interface for .ECAutoAssignment.ECAutoAssignment
    """

##code-section FOOT
##/code-section FOOT