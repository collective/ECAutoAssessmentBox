# -*- coding: utf-8 -*-
# $Id$
#
# Copyright (c) 2005 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECAutoAssessmentBox.

# Zope imports
from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

# Plone imports
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.base import updateActions, updateAliases
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.Archetypes.atapi import *
from Products.Archetypes.public import BooleanField, BooleanWidget
from Products.CMFCore.utils import getToolByName
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget \
     import ReferenceBrowserWidget

# Other product imports
from Products.ECAssignmentBox.ECAssignmentBox import ECAssignmentBox
from Products.ECAssignmentBox.ECAssignmentBox import ECAssignmentBoxSchema
from Products.ECAssignmentBox import permissions

# Local product imports
from Products.ECAutoAssessmentBox.config import *
from Products.ECAutoAssessmentBox.ECAutoAssignment import ECAutoAssignment
from Products.ECAutoAssessmentBox.DynamicDataField import DynamicDataField
from Products.ECAutoAssessmentBox.DynamicDataWidget import DynamicDataWidget



ECAutoAssessmentBoxSchema = ECAssignmentBoxSchema.copy() + Schema((

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

))

#
# This crude hack is needed because of  Plone's inflexibility in 
# changing schemas, we have to use the old name for that reason. 
#
ECAutoAssessmentBoxSchema.replaceField(
	'assignment_reference',
	ReferenceField(
        'assignment_reference',
        allowed_types = ('ECAssignmentTask','ECAutoAssessmentTask',),
        required = False,
        accessor = 'getReference',
        index = "FieldIndex:schema", # Adds "getRawAssignment_reference"
                                     # to catalog
        multiValued = False,
        relationship = 'alter_ego',
        widget = ReferenceBrowserWidget(
			description = 'Select an auto assessed assignment task.  The reference supersedes the auto assessment text and answer template below.',
            description_msgid = 'help_auto_assessment_reference',
            i18n_domain = I18N_DOMAIN,
            label = 'Reference to auto assessment task',
            label_msgid = 'label_auto_assessment_reference',
            allow_search = True,
            show_indexes = False,
        ),
    ))

finalizeATCTSchema(ECAutoAssessmentBoxSchema, folderish=True,
                   moveDiscussion=False)


class ECAutoAssessmentBox(ECAssignmentBox):
    """Automatically tests submitted assignments"""

    """
    TODO: check method security
    """

    __implements__ = (ECAssignmentBox.__implements__,)
    security = ClassSecurityInfo()

    schema = ECAutoAssessmentBoxSchema

    content_icon = ECAAB_ICON
    portal_type = meta_type = ECAAB_META
    archetype_name = ECAAB_TITLE

    # FIXME: move description to config file
    typeDescription = 'Enables the creation, submission and grading ' \
                      'of automatically tested online assignments.'
    typeDescMsgId   = 'description_edit_ecaab'

    #suppl_views = None

    filter_content_types = 1
    allowed_content_types = [ECAutoAssignment.meta_type]

    _at_rename_after_creation = True


    # -- actions ---------------------------------------------------------------
    #aliases = updateAliases(ECAssignmentBox, {
    #    'edit': 'ecaab_edit',
    #    })


    # -- methods --------------------------------------------------------------
    security.declarePrivate('getBackendDisplayList')
    def getBackendDisplayList(self):
        """
        Returns a display list of all backends selected for this site.
        """
        ecs_tool = getToolByName(self, ECS_NAME)
        return ecs_tool.getSelectedBackendsDL()


    #security.declarePrivate('_getTestsDisplayList')
    def _getTestsDisplayList(self):
        """
        Returns a display list of all available tests for a backend.
        """
        result = DisplayList(())

        ecs_tool = getToolByName(self, ECS_NAME)
        tests = ecs_tool.getBackendTestFields(self.backend)

        [result.add(key, tests[key]) for key in tests]
             
        return result
    
    def _getBackendInputFields(self):
        """
        Returns a list of field objects depending on the cached values
        for backend input fields in the spooler.
        
        TODO: Move this method to ECSpoolerTool and cache the fields so we do
              do not create them any time a auto assessment box is called in 
              edit mode.
        """
        result = []

        ecs_tool = getToolByName(self, ECS_NAME)
        fields = ecs_tool.getBackendInputFields(self.backend)
        
        for field in fields:
            # get field information
            type = fields[field].get('format', 'text')
            label = fields[field].get('label', '')
            description = fields[field].get('description', '')
            required = fields[field].get('required', False),
            # set widget
            if type in ['string',]:
                widget = StringWidget(label = label,
                            label_msgid = label,
                            description = description,
                            description_msgid = description,
                            #visible = {'edit':'visible', 'view':'invisible'},
                            i18n_domain = I18N_DOMAIN,)

                result.append(StringField(field, 
                                          widget = widget, 
                                          ), 
                              )
            elif type == 'boolean':
                widget = BooleanWidget(label = label,
                            label_msgid = label,
                            description = description,
                            description_msgid = description,
                            #visible = {'edit':'visible', 'view':'invisible'},
                            i18n_domain = I18N_DOMAIN,)

                result.append(BooleanField(field, 
                                           widget = widget, 
                                          ), 
                              )
            else:
                widget = TextAreaWidget(label = label,
                            label_msgid = label,
                            description = description,
                            description_msgid = description,
                            #visible = {'edit':'visible', 'view':'invisible'},
                            rows = 12,
                            i18n_domain = I18N_DOMAIN,)

                result.append(TextField(field, 
                                        widget = widget, 
                                        ), 
                              )

        return result
    

registerATCT(ECAutoAssessmentBox, PRODUCT_NAME)
