# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from Products.CMFCore import permissions
from Products.ATContentTypes.configuration.config import zconf

# i18n 
I18N_DOMAIN = 'eduComponents'

# dependencies of products to be installed by quick-installer
DEPENDENCIES = ['ECAssignmentBox']

# permissions
add_permission  = permissions.AddPortalContent
edit_permission = permissions.ModifyPortalContent
view_permission = permissions.View

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


# content types
#default_content_type = zconf.
#allowable_content_types = zconf.