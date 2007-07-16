# -*- coding: UTF-8 -*-
# $Id$
#
# Copyright (c) 2007 by Otto-von-Guericke-Universität, Magdeburg
#
# This file is part of ECAutoAssessmentBox.
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from Products.CMFCore import permissions
from Products.Archetypes.public import DisplayList

# FIXME: some entries are definied twice, in this config file and 
#        the one in ECAssignmentBox
#from Products.ECAssignmentBox import config

GLOBALS = globals()

# check for Plone 2.1
try:
    from Products.CMFPlone.migrations import v2_1
except ImportError:
    HAS_PLONE21 = False
else:
    HAS_PLONE21 = True

# dependencies of products to be installed by quick-installer
DEPENDENCIES = ['ECAssignmentBox', 'AddRemoveWidget']

# dependend products - not quick-installed - used in testcase
PRODUCT_DEPENDENCIES = []

# domain name used for internationalization
I18N_DOMAIN = 'eduComponents'

# define product and tool names
PRODUCT_NAME = 'ECAutoAssessmentBox'

ECAAB_NAME = 'ECAAB'
ECAAB_TITLE = 'Auto Assessment Box'
ECAAB_META = ECAAB_NAME
ECAAB_ICON = 'ecaab.png'

ECAA_NAME = 'ECAA'
ECAA_TITLE = 'Auto Assessed Assignment'
ECAA_META = ECAA_NAME
ECAA_ICON = ''

ECAAT_META = "ECAutoAssessmentTask"
ECAAT_NAME = "Auto Assessment Task"

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

# FIXME: entries are already defined in config.py in ECAssignmentBox product
ECA_WF_NAME = 'ec_assignment_workflow'
ECA_WF_TITLE = 'ECAssignment Workflow'
ECA_WF_ICON = ''

# define skins directory
SKINS_DIR = 'skins'

# define permissions (defined already in Products.CMFCore.permissions)
add_permission = permissions.AddPortalContent
edit_permission = permissions.ModifyPortalContent
view_permission = permissions.View

# FIXME: entries are already defined in config.py in ECAssignmentBox product
# define text types
TEXT_TYPES = (
    'text/structured',
    'text/x-rst',
    'text/html',
    'text/plain',
    )
