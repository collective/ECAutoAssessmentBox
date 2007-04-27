# -*- coding: utf-8 -*-
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

from StringIO import StringIO

from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.Archetypes.public import listTypes
from Products.CMFCore.utils import getToolByName

from Products.ECAutoAssessmentBox.config import *

def setuplDependencies(self, out):
    """
    Tests wether or not depending products are available and installed. If 
    not, we will try to install them.
    """
    qi = getToolByName(self, 'portal_quickinstaller')
    for product in DEPENDENCIES:
        if qi.isProductInstallable(product):
            if not qi.isProductInstalled(product):
                qi.installProduct(product)
        else:
            out.write("Warnig: Depending product '%s' ist not installable." %
                      product)


def setupECSpoolerTool(self, out):
    """ 
    Adds the ecspooler setup tool to the portal root folder.
    """
    if hasattr(self, ECS_NAME):
        self.manage_delObjects([ECS_NAME])
        out.write('Deleting old %s; make sure you repeat customizations.\n' % 
                  ECS_NAME)

    addTool = self.manage_addProduct[PRODUCT_NAME].manage_addTool
    addTool(ECS_META, None)

    # get tool for further modifications
    tool = getToolByName(self, ECS_NAME)
    # set title of tool
    tool.title = ECS_TITLE

    # write message
    out.write("Added %s to the portal root folder.\n" % ECS_NAME)


def setupProperties(self, out):
    """
    Install properties for ECSpooler/ECAutoAssessmentBox
    """
    if not hasattr(self.portal_properties, ECS_PROP_NAME):
        self.portal_properties.addPropertySheet(ECS_PROP_NAME,
                                                ECS_PROP_TITLE)
    
    props = self.portal_properties.ecspooler_properties

    if not hasattr(props, 'host'):
        props._setProperty('host', "", 'string')
        
    if not hasattr(props, 'port'):
        props._setProperty('port', "", 'int')

    if not hasattr(props, 'username'):
        props._setProperty('username', "", 'string')

    if not hasattr(props, 'password'):
        props._setProperty('password', "", 'string')
        
    if not hasattr(props, 'backends'):
        props._setProperty('backends', [], 'lines')

    out.write("Installed site-wide " + ECS_PROP_TITLE + ".\n")


def addToolToPrefsPanel(self, out):
    """
    Adds ECAutoAssessmentBox/ECSpooler setup page 
    to Plone's preferences panel
    """
    cp = getToolByName(self, 'portal_controlpanel', None)
    if not cp:
        out.write('No control panel found. Skipping registration of '
                  'the setup tool.\n')
    else:
        cp.addAction(id = ECS_PREFS_NAME,
                     name = ECS_PREFS_TITLE,
                     action = 'string:${portal_url}/prefs_spooler_form',
                     permission = 'Manage portal',
                     category = 'Products',
                     appId = PRODUCT_NAME,
                     imageUrl = ECS_PREFS_ICON,
                     description = '')

    out.write("Added '%s' to the preferences panel.\n" % ECS_PREFS_TITLE)


def removeToolFromPrefsPanel(self):
    """
    Removes ECAutoAssessmentBox/ECSpooler setup page
    from Plone's preferences panel
    """
    cp = getToolByName(self, 'portal_controlpanel', None)
    if cp:
        cp.unregisterApplication(PRODUCT_NAME)


def setupWorkflow(self, out):
    """
    Assign ECAutoAssignement objects to ec_assignment_workflow.
    """
    
    wf_tool = getToolByName(self, 'portal_workflow')
    
    if 'ec_assignment_workflow' in wf_tool.objectIds():
        wf_tool.setChainForPortalTypes((ECAA_NAME,), ECA_WF_NAME)
    
        # in case the workflows have changed, update all workflow-aware objects
        wf_tool.updateRoleMappings()
    
        out.write("Assigned '%s' to %s.\n" % (ECAA_TITLE, ECA_WF_NAME))

    else:
        out.write("Failed to assign '%' to %s.\n" % (ECAA_TITLE, ECA_WF_NAME))


def install(self):
    """
    Installs the product.
    """
    out = StringIO()

    # install depending products
    setuplDependencies(self, out)
    # install types
    installTypes(self, out, listTypes(PRODUCT_NAME), PRODUCT_NAME)
    # install subskins
    install_subskin(self, out, GLOBALS)
    # install workflows
    setupWorkflow(self, out)
    # install tools
    setupECSpoolerTool(self, out)
    # register tool to Plone's preferences panel
    addToolToPrefsPanel(self, out)
    # install site-wide properties to portal_properties
    setupProperties(self, out)

    # enable portal_factory for given types
    factory_tool = getToolByName(self, 'portal_factory')
    factory_types=[
        ECAAB_NAME,
        ECAA_NAME,
        ] + factory_tool.getFactoryTypes().keys()
    factory_tool.manage_setPortalFactoryTypes(listOfTypeIds=factory_types)

    print >> out, "Successfully installed %s." % PRODUCT_NAME
    return out.getvalue()


def uninstall(self, reinstall):
    """ 
    Uninstalls the product.
    """
    out = StringIO()

    # remove preference panel
    removeToolFromPrefsPanel(self)

    # FIXME: use a method
    if hasattr(self, ECS_NAME):
        self.manage_delObjects([ECS_NAME])
        out.write('Removed %s.\n' % ECS_NAME)
        
    # FIXME: use a method
    # remove property sheet
    if not reinstall:
        if hasattr(self.portal_properties, ECS_PROP_NAME):
            self.portal_properties.manage_delObjects(ECS_PROP_NAME)

    print >> out, "Successfully uninstalled %s." % PRODUCT_NAME
    return out.getvalue()
