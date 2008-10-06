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

# content types
#default_content_type = zconf.
#allowable_content_types = zconf.