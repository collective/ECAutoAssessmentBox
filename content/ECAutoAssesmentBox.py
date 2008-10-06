# -*- coding: utf-8 -*-
#
# File: ECAutoAssesmentBox.py
#
# Copyright (c) 2008 by []
# Generator: ArchGenXML Version 2.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.ECAutoAssessmentBox.config import *

##code-section module-header #fill in your manual code here

from Products.ECAssignmentBox.content.ECAssignmentBox import ECAssignmentBox
from Products.ECAssignmentBox.content.ECAssignmentBox import ECAssignmentBox_schema
# FIXME:
#from Products.ECAssignmentBox import permissions

from Products.ECAutoAssessmentBox.ECAutoAssignment import ECAutoAssignment
from Products.ECAutoAssessmentBox.DynamicDataField import DynamicDataField
from Products.ECAutoAssessmentBox.DynamicDataWidget import DynamicDataWidget


##/code-section module-header

schema = Schema((

    StringField(
        'backend',
        required = True,
        vocabulary = 'getBackendDisplayList',
        widget = SelectionWidget(
            modes=('edit'),
            label='Test backend',
            label_msgid='label_backend',
            description='Select a test backend.',
            description_msgid='help_backend',
            i18n_domain=I18N_DOMAIN,
        ),
        read_permission = permissions.ModifyPortalContent,
    ),
    
    BooleanField(
        'autoAccept',
        default = False,
        #required = True,
        widget = BooleanWidget(
            label = 'Automatically accept assignments',
            label_msgid = 'label_auto_accept',
            description = 'If selected, an assignment which passes all tests will be automatically accepted.',
            description_msgid = 'help_auto_accept',
            i18n_domain = I18N_DOMAIN,
        ),
        schemata = 'backend',
        read_permission = permissions.ModifyPortalContent,
    ),

    StringField(
        'tests',
        #required = True,
        vocabulary = '_getTestsDisplayList',
        widget = MultiSelectionWidget(
            modes=('edit'),
            label='Tests',
            label_msgid='label_tests',
            description='Select one or more tests.',
            description_msgid='help_tests',
            i18n_domain=I18N_DOMAIN,
        ),
        schemata = 'backend',
        read_permission = permissions.ModifyPortalContent,
    ),

    # FIXME: comment in if available
    """
    DynamicDataField('inputFields',
        #required = True,
        schemata = 'backend',
        fields = '_getBackendInputFields',
        widget = DynamicDataWidget(
            visible = {'edit':'visible', 'view':'invisible'},
            label = "Input fields",
            description = 'Input fields for a backend',
            label_msgid = 'label_input_field',
            description_msgid = 'help_input_field',
            i18n_domain = I18N_DOMAIN,
        ),
        read_permission = permissions.ModifyPortalContent,
    ),
    """

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ECAutoAssesmentBox_schema = ECAssignmentBox_schema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class ECAutoAssesmentBox(ECAssignmentBox):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IECAutoAssesmentBox)

    meta_type = 'ECAutoAssesmentBox'
    _at_rename_after_creation = True

    schema = ECAutoAssesmentBox_schema

    # FIXME: allowed_content_types is defined in profile.default.types.ECAutoAssessmentBox.xml
    #        and should be used elsewhere
    allowed_content_types = ['ECAutoAssignment']

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    #security.declarePrivate('getBackendDisplayList')
    def getBackendDisplayList(self):
        """
        Returns a display list of all backends selected for this site.
        """
        # FIXME: comment in if tool is working
        """
        ecs_tool = getToolByName(self, ECS_NAME)
        return ecs_tool.getSelectedBackendsDL()
        """
        
        return DisplayList(())


    #security.declarePrivate('_getTestsDisplayList')
    def _getTestsDisplayList(self):
        """
        Returns a display list of all available tests for a backend.
        """
        result = DisplayList(())

        # FIXME: comment in if tool is working
        """
        ecs_tool = getToolByName(self, ECS_NAME)
        tests = ecs_tool.getBackendTestFields(self.backend)

        [result.add(key, tests[key]) for key in tests]
        """
             
        return result
    
    #security.declarePrivate('_getBackendInputFields')
    def _getBackendInputFields(self):
        """
        Returns a list of field objects depending on the cached values
        for backend input fields in the spooler.
        
        TODO: Move this method to ECSpoolerTool and cache the fields so we do
              do not create them any time a auto assessment box is called in 
              edit mode.
        """
        result = []

        # FIXME: comment in if tool is working
#        ecs_tool = getToolByName(self, ECS_NAME)
#        fields = ecs_tool.getBackendInputFields(self.backend)
#        
#        for field in fields:
#            # get field information
#            type = fields[field].get('format', 'text')
#            label = fields[field].get('label', '')
#            description = fields[field].get('description', '')
#            required = fields[field].get('required', False),
#            # set widget
#            if type in ['string',]:
#                widget = StringWidget(label = label,
#                            label_msgid = label,
#                            description = description,
#                            description_msgid = description,
#                            #visible = {'edit':'visible', 'view':'invisible'},
#                            i18n_domain = I18N_DOMAIN,)
#
#                result.append(StringField(field, 
#                                          widget = widget, 
#                                          ), 
#                              )
#            elif type == 'boolean':
#                widget = BooleanWidget(label = label,
#                            label_msgid = label,
#                            description = description,
#                            description_msgid = description,
#                            #visible = {'edit':'visible', 'view':'invisible'},
#                            i18n_domain = I18N_DOMAIN,)
#
#                result.append(BooleanField(field, 
#                                           widget = widget, 
#                                          ), 
#                              )
#            else:
#                widget = TextAreaWidget(label = label,
#                            label_msgid = label,
#                            description = description,
#                            description_msgid = description,
#                            #visible = {'edit':'visible', 'view':'invisible'},
#                            rows = 12,
#                            i18n_domain = I18N_DOMAIN,)
#
#                result.append(TextField(field, 
#                                        widget = widget, 
#                                        ), 
#                              )
        
        return result

registerType(ECAutoAssesmentBox, PROJECTNAME)
# end of class ECAutoAssesmentBox

##code-section module-footer #fill in your manual code here
##/code-section module-footer


