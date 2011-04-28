# -*- coding: utf-8 -*-
# $Id:ECAutoAssessmentBox.py 1311 2009-09-28 07:03:00Z amelung $
#
# Copyright (c) 2006-2010 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECAutoAssessmentBox.
#
__author__ = """Mario Amelung <mario.amelung@gmx.de>"""
__docformat__ = 'plaintext'
__version__   = '$Revision:1311 $'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope import interface
from zope.interface import implements
import interfaces

from Products.Archetypes.interfaces import IMultiPageSchema
from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.ECAutoAssessmentBox.config import *

##code-section module-header #fill in your manual code here
import logging

from Products.ECAssignmentBox.content.ECAssignmentBox import ECAssignmentBox
from Products.ECAssignmentBox.content.ECAssignmentBox import ECAssignmentBox_schema
#from Products.ECAssignmentBox import permissions

from Products.ECAutoAssessmentBox.content.ECAutoAssignment import ECAutoAssignment
from Products.ECAutoAssessmentBox.content.DynamicDataField import DynamicDataField
from Products.ECAutoAssessmentBox.content.DynamicDataWidget import DynamicDataWidget


logger = logging.getLogger('ECAutoAssessmentBox')

##/code-section module-header

schema = Schema((

    StringField(
        'backend',
        required = True,
        vocabulary = 'getBackendDisplayList',
        widget = SelectionWidget(
            format='select',
            modes=('edit'),
            label='Test backend',
            label_msgid='label_backend',
            description='Select a test backend.',
            description_msgid='help_backend',
            i18n_domain=I18N_DOMAIN,
        ),
        schemata = 'backend',
        read_permission = 'Modify Portal Content',
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
        read_permission = 'Modify Portal Content',
    ),

    StringField(
        'tests',
        required = True,
        vocabulary = '_getTestsDisplayList',
        widget = MultiSelectionWidget(
            modes=('edit'),
            label='Tests',
            label_msgid='label_tests',
            description='Select one or more tests.',
            description_msgid='help_tests',
            i18n_domain=I18N_DOMAIN,
            macro="widget_select_backend_tests",
        ),
        schemata = 'backend',
        read_permission = 'Modify Portal Content',
    ),

    DynamicDataField('inputFields',
        #required = True,
        fields = '_getBackendInputFields',
        widget = DynamicDataWidget(
            visible = {'edit':'visible', 'view':'invisible'},
            label = "Input fields",
            description = 'Input fields for a backend',
            label_msgid = 'label_input_field',
            description_msgid = 'help_input_field',
            i18n_domain = I18N_DOMAIN,
        ),
        schemata = 'backend',
        read_permission = 'Modify Portal Content',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ECAutoAssessmentBox_schema = ECAssignmentBox_schema.copy() + \
    schema.copy()

ECAutoAssessmentBox_schema['id'].widget.visible = dict(edit=0, view=0)



class ECAutoAssessmentBox(ECAssignmentBox):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IECAutoAssessmentBox)

    meta_type = 'ECAAB'
    _at_rename_after_creation = True

    schema = ECAutoAssessmentBox_schema

    ##code-section class-header #fill in your manual code here

    # FIXME: allowed_content_types is defined in profile.default.types.ECAutoAssessmentBox.xml
    #        and should be used elsewhere
    allowed_content_types = ['ECAA']
    
    # Methods
    #security.declarePrivate('getBackendDisplayList')
    def getBackendDisplayList(self):
        """
        Returns a display list of all backends selected for this site.
        """
        ecs_tool = getToolByName(self, ECS_NAME)
        return ecs_tool.getSelectedBackendsDL()


    #security.declarePrivate('_getTestsDisplayList')
    def _getTestsDisplayList(self, backend=None):
        """
        Returns a display list of all available tests for a backend.
        """
        result = DisplayList(())

        if (backend == None):
            backend = self.backend

        ecs_tool = getToolByName(self, ECS_NAME)
        tests = ecs_tool.getBackendTestFields(backend)

        [result.add(key, tests[key]) for key in tests]
             
        return result
    
    #security.declarePrivate('_getBackendInputFields')
    def _getBackendInputFields(self, backend=None):
        """
        Returns a list of field objects depending on the cached values
        for backend input fields in the spooler.
        
        TODO: Move this method to ECSpoolerTool and cache the fields so we do
              do not create them any time a auto assessment box is called in 
              edit mode.
        """
        result = []
        
        if (backend == None):
            backend = self.backend

        ecs_tool = getToolByName(self, ECS_NAME)
        fields = ecs_tool.getBackendInputFields(backend)
        
        for field in fields:
            
            # get field information
            type = fields[field].get('format', 'text')
            label = fields[field].get('label', '')
            description = fields[field].get('description', '')
            required = fields[field].get('required', False)
            
            # set widget
            # StringField
            if type in ['string',]:
                widget = StringWidget(label = label,
                            label_msgid = label,
                            description = description,
                            description_msgid = description,
                            #visible = {'edit':'visible', 'view':'invisible'},
                            i18n_domain = I18N_DOMAIN,)

                result.append(StringField(field,
                                          required = required, 
                                          widget = widget, 
                                          ),
                             ) 
            # BooleanField                  
            elif type == 'boolean':
                widget = BooleanWidget(label = label,
                            label_msgid = label,
                            description = description,
                            description_msgid = description,
                            #visible = {'edit':'visible', 'view':'invisible'},
                            i18n_domain = I18N_DOMAIN,)

                result.append(BooleanField(field,
                                           required = required,
                                           widget = widget, 
                                          ), 
                              )
            # TextField for all others
            else:
                widget = TextAreaWidget(label = label,
                            label_msgid = label,
                            description = description,
                            description_msgid = description,
                            #visible = {'edit':'visible', 'view':'invisible'},
                            rows = 12,
                            i18n_domain = I18N_DOMAIN,)

                result.append(TextField(field,
                                        required = required, 
                                        widget = widget, 
                                        ), 
                              )
        
        return result

interface.alsoProvides(ECAutoAssessmentBox, IMultiPageSchema)

registerType(ECAutoAssessmentBox, PROJECTNAME)
# end of class ECAutoAssessmentBox

##code-section module-footer #fill in your manual code here
##/code-section module-footer


