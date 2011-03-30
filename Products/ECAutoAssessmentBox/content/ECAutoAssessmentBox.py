# -*- coding: utf-8 -*-
# $Id:ECAutoAssessmentBox.py 1311 2009-09-28 07:03:00Z amelung $
#
# Copyright (c) 2006-2011 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECAutoAssessmentBox.
#
from symbol import try_stmt
__author__ = """Mario Amelung <mario.amelung@gmx.de>"""
__docformat__ = 'plaintext'
__version__   = '$Revision:1311 $'

import interfaces

from Acquisition import aq_inner

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope import interface
from zope.interface import implements

from Products.Archetypes.interfaces import IMultiPageSchema
from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema

from Products.ECAutoAssessmentBox import config
from Products.ECAutoAssessmentBox import LOG

from Products.ECAssignmentBox.content.ECAssignmentBox import ECAssignmentBox
from Products.ECAssignmentBox.content.ECAssignmentBox import ECAssignmentBox_schema
#from Products.ECAssignmentBox import permissions

from Products.ECAutoAssessmentBox.content.ECAutoAssignment import ECAutoAssignment
from Products.ECAutoAssessmentBox.content.DynamicDataField import DynamicDataField
from Products.ECAutoAssessmentBox.content.DynamicDataWidget import DynamicDataWidget


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
            i18n_domain=config.I18N_DOMAIN,
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
            i18n_domain = config.I18N_DOMAIN,
        ),
        schemata = 'backend',
        read_permission = 'Modify Portal Content',
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
            i18n_domain=config.I18N_DOMAIN,
            macro="widget_select_backend_tests"
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
            i18n_domain = config.I18N_DOMAIN,
        ),
        schemata = 'backend',
        read_permission = 'Modify Portal Content',
    ),

),
)

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
        ecaab_utils = getToolByName(self, config.ECS_NAME)
        return ecaab_utils.getSelectedBackendsDL()


    #security.declarePrivate('_getTestsDisplayList')
    def _getTestsDisplayList(self, backend=None):
        """
        Returns a display list of all available tests for a backend.
        """
        result = DisplayList(())

        if (backend == None):
            backend = self.backend

        ecaab_utils = getToolByName(self, config.ECS_NAME)
        tests = ecaab_utils.getBackendTestFields(backend)

        [result.add(key, tests[key]) for key in tests]
             
        return result
    
    #security.declarePrivate('_getBackendInputFields')
    def _getBackendInputFields(self, backend=None):
        """
        Returns a list of field objects depending on the cached
        values for backend's input fields.
        
        TODO, 2011-03-26, ma: 
        Move this method to ECSpoolerTool and cache the fields so we
        do not create them any time a auto assessment box is called 
        in edit mode.
        """
        result = []
        
        if (backend == None):
            backend = self.backend
        
        ecaab_utils = getToolByName(self, config.ECS_NAME)
        fields = ecaab_utils.getBackendInputFields(backend)
        
        for field in fields:
            # get field information
            type = fields[field].get('format', 'text')
            label = fields[field].get('label', '')
            description = fields[field].get('description', '')
            required = fields[field].get('required', False),
            
            # set widget
            # StringField
            if type in ['string',]:
                widget = StringWidget(label = label,
                            label_msgid = label,
                            description = description,
                            description_msgid = description,
                            #visible = {'edit':'visible', 'view':'invisible'},
                            i18n_domain = config.I18N_DOMAIN,)

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
                            i18n_domain = config.I18N_DOMAIN,)

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
                            i18n_domain = config.I18N_DOMAIN,)

                result.append(
                    TextField(field, 
                              required = required, 
                              allowable_content_types = (config.EC_DEFAULT_MIME_TYPE,), 
                              default_content_type = config.EC_DEFAULT_MIME_TYPE, 
                              default_output_type = config.EC_DEFAULT_FORMAT,
                              widget = widget, 
                             ), 
                    )
        
        return result

interface.alsoProvides(ECAutoAssessmentBox, IMultiPageSchema)

registerType(ECAutoAssessmentBox, config.PROJECTNAME)
