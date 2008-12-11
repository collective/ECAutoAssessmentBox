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
__version__   = '$Revision$'

# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from Products.CMFCore.permissions import setDefaultRoles
##code-section config-head #fill in your manual code here
##/code-section config-head


PROJECTNAME = "ECAutoAssessmentBox"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
ADD_CONTENT_PERMISSIONS = {
    'ECAutoAssessmentBox': 'ECAutoAssessmentBox: Add ECAutoAssessmentBox',
    'ECAutoAssignment': 'ECAutoAssessmentBox: Add ECAutoAssignment',
}

setDefaultRoles('ECAutoAssessmentBox: Add ECAutoAssessmentBox', ('Manager','Owner'))
setDefaultRoles('ECAutoAssessmentBox: Add ECAutoAssignment', ('Manager','Owner'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

##code-section config-bottom #fill in your manual code here
##/code-section config-bottom


# Load custom configuration not managed by archgenxml
try:
    from Products.ECAutoAssessmentBox.AppConfig import *
except ImportError:
    pass
