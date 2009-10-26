# -*- coding: utf-8 -*-
# $Id:__init__.py 1313 2009-09-28 07:03:29Z amelung $
#
# Copyright (c) 2006-2009 Otto-von-Guericke University Magdeburg
#
# This file is part of ECAutoAssessmentBox.
#
__author__ = """Mario Amelung <mario.amelung@gmx.de>"""
__docformat__ = 'plaintext'
__version__   = '$Revision:1313 $'

# There are three ways to inject custom code here:
#
#   - To set global configuration variables, create a file AppConfig.py.
#       This will be imported in config.py, which in turn is imported in
#       each generated class and in this file.
#   - To perform custom initialisation after types have been registered,
#       use the protected code section at the bottom of initialize().

import logging
logger = logging.getLogger('ECAutoAssessmentBox')
logger.debug('Installing Product')

import sys
import os
import os.path

from Globals import package_home

from zope.i18nmessageid import MessageFactory

import Products.CMFPlone.interfaces
from Products.Archetypes import listTypes
from Products.Archetypes.atapi import *
from Products.Archetypes.utils import capitalize
from Products.CMFCore import DirectoryView
from Products.CMFCore import permissions as cmfpermissions
from Products.CMFCore import utils as cmfutils
from Products.CMFPlone.utils import ToolInit

from Products.ECAutoAssessmentBox import content
from Products.ECAutoAssessmentBox import tool
from Products.ECAutoAssessmentBox.config import *

ECMessageFactory = MessageFactory('eduComponents')

DirectoryView.registerDirectory('skins', product_globals)

# special code which provides migration of auto assessment boxes 
# created with 1.0 
sys.modules['Products.ECAutoAssessmentBox.ECAutoAssessmentBox'] = content.ECAutoAssessmentBox
sys.modules['Products.ECAutoAssessmentBox.ECAutoAssignment'] = content.ECAutoAssignment
sys.modules['Products.ECAutoAssessmentBox.ECSpoolerTool'] = tool.ECSpoolerTool

##code-section custom-init-head #fill in your manual code here
##/code-section custom-init-head

def initialize(context):
    """initialize product (called by zope)"""
    ##code-section custom-init-top #fill in your manual code here
    ##/code-section custom-init-top

    # imports packages and types for registration
    import content
    import tool

    # Initialize portal tools
    tools = [tool.ECSpoolerTool.ECSpoolerTool]
    ToolInit( PROJECTNAME +' Tools',
                tools = tools,
                icon  = 'ec_tool.png'
                ).initialize(context)

    # Initialize portal content
    all_content_types, all_constructors, all_ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = all_content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = all_constructors,
        fti                = all_ftis,
        ).initialize(context)

    # Give it some extra permissions to control them on a per class limit
    for i in range(0,len(all_content_types)):
        klassname=all_content_types[i].__name__
        if not klassname in ADD_CONTENT_PERMISSIONS:
            continue

        context.registerClass(meta_type   = all_ftis[i]['meta_type'],
                              constructors= (all_constructors[i],),
                              permission  = ADD_CONTENT_PERMISSIONS[klassname])

    ##code-section custom-init-bottom #fill in your manual code here
    ##/code-section custom-init-bottom

