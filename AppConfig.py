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
__author__ = """Mario Amelung <mario.amelung@gmx.de>"""
__docformat__ = 'plaintext'

from Products.CMFCore import permissions
from Products.ATContentTypes.configuration.config import zconf

# load custom configuration from product ECAssignmentBox
try:
    from Products.ECAssignmentBox.AppConfig import *
except ImportError:
    pass

# dependencies of products to be installed by quick-installer
DEPENDENCIES = ['ECAssignmentBox']

# define tool names
ECS_NAME = 'ecspooler_tool'
ECS_META = ECS_NAME
ECS_TITLE = 'Auto Assessment Settings'
ECS_ICON = 'ec_tool.png'

ECS_PREFS_NAME = "ecspooler_setup"
ECS_PREFS_META = ECS_PREFS_NAME
ECS_PREFS_TITLE = "Auto Assessment Settings"
ECS_PREFS_ICON = ECS_ICON

ECS_PROP_NAME = "ecspooler_properties"
ECS_PROP_META = ECS_PREFS_NAME
ECS_PROP_TITLE = "Auto Assessment Properties"

# permissions
#add_permission  = permissions.AddPortalContent
#edit_permission = permissions.ModifyPortalContent
#view_permission = permissions.View
