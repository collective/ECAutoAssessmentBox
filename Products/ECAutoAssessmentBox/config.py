# -*- coding: utf-8 -*-
# $Id:config.py 1313 2009-09-28 07:03:29Z amelung $
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
__version__   = '$Revision:1313 $'

# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.
from Products.CMFCore import permissions
from Products.ATContentTypes.configuration.config import zconf

# load custom configuration from product ECAssignmentBox
try:
    from Products.ECAssignmentBox.config import *
except ImportError:
    pass


PROJECTNAME = "ECAutoAssessmentBox"

PRODUCT_GLOBALS = globals()


# define tool names
ECS_NAME = 'ecaab_utils'
ECS_META = ECS_NAME
ECS_TITLE = 'Auto Assessment Settings'
ECS_ICON = 'ec_tool.png'

ECS_PREFS_NAME = "ecspooler_setup"
ECS_PREFS_META = ECS_PREFS_NAME
ECS_PREFS_TITLE = "Auto Assessment Settings"
ECS_PREFS_ICON = ECS_ICON

ECS_PROP_NAME = "ecaab_properties"
ECS_PROP_META = ECS_PREFS_NAME
ECS_PROP_TITLE = "Auto Assessment Properties"


# Dependend products - installed by quick-installer
DEPENDENCIES = ['ECAssignmentBox']

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []


# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
permissions.setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
ADD_CONTENT_PERMISSIONS = {
    'ECAutoAssessmentBox': 'ECAutoAssessmentBox: Add ECAutoAssessmentBox',
    'ECAutoAssignment': 'ECAutoAssessmentBox: Add ECAutoAssignment',
}

permissions.setDefaultRoles('ECAutoAssessmentBox: Add ECAutoAssessmentBox', ('Manager','Owner'))
permissions.setDefaultRoles('ECAutoAssessmentBox: Add ECAutoAssignment', ('Manager','Owner'))
