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

import os
import transaction
import logging
log = logging.getLogger('ECAutoAssessmentBox: setuphandlers')

from Products.ECAutoAssessmentBox.config import PROJECTNAME
from Products.ECAutoAssessmentBox.config import DEPENDENCIES
from Products.CMFCore.utils import getToolByName
##code-section HEAD
##/code-section HEAD

def isNotECAutoAssessmentBoxProfile(context):
    return context.readDataFile("ECAutoAssessmentBox_marker.txt") is None


def setupHideToolsFromNavigation(context):
    """hide tools"""
    
    #log.info('Hiding tools')

    if isNotECAutoAssessmentBoxProfile(context): return 
    # uncatalog tools
    site = context.getSite()
    toolnames = ['ecspooler_tool']
    portalProperties = getToolByName(site, 'portal_properties')
    navtreeProperties = getattr(portalProperties, 'navtree_properties')
    if navtreeProperties.hasProperty('idsNotToList'):
        for toolname in toolnames:
            try:
                portal[toolname].unindexObject()
            except:
                pass
            current = list(navtreeProperties.getProperty('idsNotToList') or [])
            if toolname not in current:
                current.append(toolname)
                kwargs = {'idsNotToList': current}
                navtreeProperties.manage_changeProperties(**kwargs)


def fixTools(context):
    """do post-processing on auto-installed tool instances"""
    
    #log.info('Fixing tools')

    if isNotECAutoAssessmentBoxProfile(context): return 
    site = context.getSite()
    tool_ids=['portal_ecspoolertool']
    for tool_id in tool_ids:
	    if hasattr(site, tool_id):
	        tool=site[tool_id]
	        tool.initializeArchetype()



def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    
    #log.info('Updating role mappings')

    if isNotECAutoAssessmentBoxProfile(context): return 
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()


def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    
    #log.info('Doing post install')

    if isNotECAutoAssessmentBoxProfile(context): return 
    
    reindexIndexes(context)


##code-section FOOT

def installGSDependencies(context):
    """Install dependend profiles."""

    if isNotECAutoAssessmentBoxProfile(context): return 
    
    # Has to be refactored as soon as generic setup allows a more 
    # flexible way to handle dependencies.
    
    return


def installQIDependencies(context):
    """Install dependencies"""

    if isNotECAutoAssessmentBoxProfile(context): return 
    
    site = context.getSite()

    portal = getToolByName(site, 'portal_url').getPortalObject()
    quickinstaller = portal.portal_quickinstaller
    for dependency in DEPENDENCIES:
        if quickinstaller.isProductInstalled(dependency):
            log.info('Reinstalling dependency %s:' % dependency)
            quickinstaller.reinstallProducts([dependency])
            transaction.savepoint()
        else:
            log.info('Installing dependency %s:' % dependency)
            quickinstaller.installProduct(dependency)
            transaction.savepoint()

        #quickinstaller.installProduct(dependency)
        #transaction.savepoint() 


def reindexIndexes(context):
    """Reindex some indexes.

    Indexes that are added in the catalog.xml file get cleared
    everytime the GenericSetup profile is applied.  So we need to
    reindex them.

    Since we are forced to do that, we might as well make sure that
    these get reindexed in the correct order.
    """
    if isNotECAutoAssessmentBoxProfile(context): return 

    site = context.getSite()

    pc = getToolByName(site, 'portal_catalog')
    indexes = [
        'isAssignmentBoxType',
        'isAssignmentType',
        'getRawAssignment_reference',
        'getRawRelatedItems',
        'review_state',
        ]
    # Don't reindex an index if it isn't actually in the catalog.
    # Should not happen, but cannot do any harm.
    ids = [id for id in indexes if id in pc.indexes()]
    if ids:
        pc.manage_reindexIndex(ids=ids)
    
    log.info('Reindexed %s' % indexes)

##/code-section FOOT
