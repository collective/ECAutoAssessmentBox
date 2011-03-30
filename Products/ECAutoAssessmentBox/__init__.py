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

#from Globals import package_home
#from App.Common import package_home

from zope.i18nmessageid import MessageFactory

import Products.CMFPlone.interfaces
from Products.Archetypes import listTypes
from Products.Archetypes.atapi import *
from Products.Archetypes.utils import capitalize
from Products.CMFCore import DirectoryView
from Products.CMFCore import permissions as cmfpermissions
from Products.CMFCore import utils as cmfutils
from Products.CMFPlone.utils import ToolInit

from Products.ECAutoAssessmentBox import config

LOG = logging.getLogger(config.PROJECTNAME)

ECMessageFactory = MessageFactory('eduComponents')

DirectoryView.registerDirectory('skins', config.PRODUCT_GLOBALS)

# special code which provides migration of auto assessment boxes 
# created with 1.0 
from Products.ECAutoAssessmentBox import content
from Products.ECAutoAssessmentBox import tool

sys.modules['Products.ECAutoAssessmentBox.ECAutoAssessmentBox'] = content.ECAutoAssessmentBox
sys.modules['Products.ECAutoAssessmentBox.ECAutoAssignment'] = content.ECAutoAssignment
sys.modules['Products.ECAutoAssessmentBox.ECSpoolerTool'] = tool.ECSpoolerTool


def initialize(context):
    """initialize product (called by zope)
    """

    # imports packages and types for registration
    #import content
    #import tool

    # Initialize portal tools
    tools = [tool.ECSpoolerTool.ECSpoolerTool]
    ToolInit(config.PROJECTNAME +' Tools',
                tools = tools,
                icon  = 'ec_tool.png'
                ).initialize(context)

    # Initialize portal content
    all_content_types, all_constructors, all_ftis = process_types(
        listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    cmfutils.ContentInit(
        config.PROJECTNAME + ' Content',
        content_types      = all_content_types,
        permission         = config.DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = all_constructors,
        fti                = all_ftis,
        ).initialize(context)

    # Give it some extra permissions to control them on a per class limit
    for i in range(0,len(all_content_types)):
        klassname=all_content_types[i].__name__
        if not klassname in config.ADD_CONTENT_PERMISSIONS:
            continue

        context.registerClass(meta_type   = all_ftis[i]['meta_type'],
                              constructors= (all_constructors[i],),
                              permission  = config.ADD_CONTENT_PERMISSIONS[klassname])

