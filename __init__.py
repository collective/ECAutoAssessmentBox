# -*- coding: UTF-8 -*-
# $Id$
#
# Copyright (c) 2005 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECAutoAssessmentBox.
import os, os.path

from Globals import package_home

from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory

# local imports
from config import *

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):
    """
    """
    # Import Types here to register them
    import ECAutoAssessmentBox, ECAutoAssignment, ECAutoAssessmentTask

    from AccessControl import ModuleSecurityInfo
    from AccessControl import allow_module, allow_class, allow_type

    content_types, constructors, ftis = process_types(
        listTypes(PRODUCT_NAME),
        PRODUCT_NAME)
    
    utils.ContentInit(
        PRODUCT_NAME + ' Content',
        content_types      = content_types,
        permission         = add_permission,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    # Import tools here to register them
    from ECSpoolerTool import ECSpoolerTool
    from Products.CMFPlone.utils import ToolInit

    tools = (ECSpoolerTool,)
    
    ToolInit(PRODUCT_NAME + ' Tool',
        tools = tools,
        product_name = PRODUCT_NAME,
        icon = ECS_ICON
        ).initialize(context)
