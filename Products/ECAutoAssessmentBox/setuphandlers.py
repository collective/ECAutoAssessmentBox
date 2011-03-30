# -*- coding: utf-8 -*-
# $Id$
#
# Copyright (c) 2006-2011 Otto-von-Guericke-Universität Magdeburg
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

import transaction
import logging
log = logging.getLogger('ECAutoAssessmentBox: setuphandlers')

from Products.CMFCore.utils import getToolByName

from Products.ECAutoAssessmentBox import config
from Products.ECAutoAssessmentBox import LOG


def isNotECAutoAssessmentBoxProfile(context):
    """Read marker file
    """
    return context.readDataFile("ECAutoAssessmentBox_marker.txt") is None


def setupHideToolsFromNavigation(context):
    """Hide ecaab_utils from navigation
    """
    
    if isNotECAutoAssessmentBoxProfile(context): return 

    LOG.info("Hiding '%s' from navigation" % config.ECS_NAME)

    # uncatalog ecaab_utils
    toolnames = [config.ECS_NAME]

    site = context.getSite()
    portal = getToolByName(site, 'portal_url').getPortalObject()

    portalProperties = getToolByName(site, 'portal_properties')
    navtreeProperties = getattr(portalProperties, 'navtree_properties')
    
    if navtreeProperties.hasProperty('idsNotToList'):
        current = list(navtreeProperties.getProperty('idsNotToList') or [])
        # add all ids 
        for toolname in toolnames:
            if toolname not in current:
                current.append(toolname)
                kwargs = {'idsNotToList': current}
                navtreeProperties.manage_changeProperties(**kwargs)

        for item in current:
            try:
                portal[item].unindexObject()
            except:
                LOG.warn('Could not unindex object: %s' % item)


def fixTools(context):
    """Do post-processing on ecaab_utils
    """
    if isNotECAutoAssessmentBoxProfile(context): return 

    LOG.info("Fixing '%s' after installation" % config.ECS_NAME)

    site = context.getSite()
    
    if hasattr(site, config.ECS_NAME):
        tool = site[config.ECS_NAME]
        tool.initializeArchetype()


def updateRoleMappings(context):
    """After workflow has changed update the roles mapping. This 
    is like pressing the button 'Update Security Setting' at portal_workflow
    """

    if isNotECAutoAssessmentBoxProfile(context): return 
    
    LOG.info('Updating role mappings')

    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()


def postInstall(context):
    """Called at the end of the setup process (the right place for 
    your custom code). 
    """
    
    if isNotECAutoAssessmentBoxProfile(context): return 
    
    LOG.info('Post installation...')
    reindexIndexes(context)


def installGSDependencies(context):
    """Install dependend profiles.
    """

    if isNotECAutoAssessmentBoxProfile(context): return 
    
    # Has to be refactored as soon as generic setup allows a more 
    # flexible way to handle dependencies.
    return


def installQIDependencies(context):
    """Install dependencies
    """

    if isNotECAutoAssessmentBoxProfile(context): return 
    
    LOG.info("Installing QI dependencies...")

    site = context.getSite()

    portal = getToolByName(site, 'portal_url').getPortalObject()
    quickinstaller = portal.portal_quickinstaller
    for dependency in config.DEPENDENCIES:
        if quickinstaller.isProductInstalled(dependency):
            LOG.info('Reinstalling dependency %s:' % dependency)
            quickinstaller.reinstallProducts([dependency])
            transaction.savepoint()
        else:
            LOG.info('Installing dependency %s:' % dependency)
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
    
    LOG.info('Reindexed %s' % indexes)
