# -*- coding: utf-8 -*-
#
# Copyright (c) 2006 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECAssignmentBox.
#
# ECAssignmentBox is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# ECAssignmentBox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ECAssignmentBox; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA
#
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *
from Products.Archetypes.public import BooleanField, BooleanWidget
from Products.ATContentTypes.content.base import registerATCT,updateAliases,updateActions
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.folder import ATFolderSchema,ATFolder

from Products.ECAutoAssessmentBox.PlainTextField import PlainTextField
from Products.ECAutoAssessmentBox.config import *
from Products.ECAutoAssessmentBox.DynamicDataField import DynamicDataField
from Products.ECAutoAssessmentBox.DynamicDataWidget import DynamicDataWidget



ECAutoAssessmentTaskSchema = ATFolderSchema.copy() + Schema((
	TextField('assignment_text',
		required = True,
		searchable = True,
		default_output_type = 'text/html',
		default_content_type = 'text/structured',
		allowable_content_types = TEXT_TYPES,
		widget = RichWidget(
			label = 'Assignment text',
			label_msgid = 'label_assignment_text',
			description = 'Enter text and hints for the assignment',
			description_msgid = 'help_assignment_text',
			i18n_domain = I18N_DOMAIN,
			rows=10,
		),
	),
	PlainTextField('answerTemplate',
		widget = RichWidget(
			label = 'Answer template',
			label_msgid = 'label_answer_template',
			description = 'You can provide a template for the students\' answers',
			description_msgid = 'help_answer_template',
			i18n_domain = I18N_DOMAIN,
			rows = 12,
			format = 0,
		),
	),
    StringField('backend',
        required = True,
        vocabulary = 'getBackendDisplayList',
        read_permission = permissions.ModifyPortalContent,
        widget = SelectionWidget(
            modes=('edit'),
            label='Test backend',
            label_msgid='label_backend',
            description='Select a test backend.',
            description_msgid='help_backend',
            i18n_domain=I18N_DOMAIN,
        ),
    ),
    BooleanField(
        'autoAccept',
        default = False,
        schemata = 'backend',
        read_permission = permissions.ModifyPortalContent,
        widget = BooleanWidget(
            label = 'Automatically accept assignments',
            label_msgid = 'label_auto_accept',
            description = 'If selected, an assignment which passes all tests will be automatically accepted.',
            description_msgid = 'help_auto_accept',
            i18n_domain = I18N_DOMAIN,
        ),
    ),
    StringField('tests',
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
        fields = '_getBackendInputFields',
        schemata = 'backend',
        read_permission = permissions.ModifyPortalContent,
        widget = DynamicDataWidget(
            visible = {'edit':'visible', 'view':'invisible'},
            label = "Input fields",
            description = 'Input fields for a backend',
            label_msgid = 'label_input_field',
            description_msgid = 'help_input_field',
            i18n_domain = I18N_DOMAIN,
        ),
    ),
))

finalizeATCTSchema(ECAutoAssessmentTaskSchema)



class ECAutoAssessmentTask(ATFolder):
	"""Assignment task for an auto assessment box.
	"""

	portal_type = meta_type = ECAAT_META
	archetype_name = ECAAT_NAME
	content_icon = 'ecaat.png'
	schema = ECAutoAssessmentTaskSchema
	typeDescription = 'Enables the creation, submission and grading of automatically tested online assignments.'
	typeDescMsgId   = 'description_edit_ecaab'


	_at_rename_after_creation = True
	__implements__ = ATFolder.__implements__
	security = ClassSecurityInfo()

	# Attach views
	default_view = 'ecaat_view'
	immediate_view = 'ecaat_view'
	suppl_views = None

	actions = updateActions(ATFolder, ({
			'action':      'string:$object_url/ecat_backlinks',
			'category':    'object',
			'id':          'ecat_backlinks',
			'name':        'Backlinks',
			'permissions': (permissions.ManageProperties,),
		},))


	aliases = updateAliases(ATFolder, {
		'view'		: 'ecaat_view',
	})

	# -- methods --------------------------------------------------------------
	security.declarePrivate('getBackendDisplayList')
	def getBackendDisplayList(self):
		"""Returns a display list of all backends selected for this site.
		"""
		ecs_tool = getToolByName(self, ECS_NAME)
		return ecs_tool.getSelectedBackendsDL()

	#security.declarePrivate('_getTestsDisplayList')
	def _getTestsDisplayList(self):
		"""Returns a display list of all available tests for a backend.
		"""
		result = DisplayList(())
		ecs_tool = getToolByName(self, ECS_NAME)
		tests = ecs_tool.getBackendTestFields(self.backend)
		[result.add(key, tests[key]) for key in tests]
		return result

	def _getBackendInputFields(self):
		"""Returns a list of field objects depending on the cached values
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
				result.append(StringField(field,widget = widget,),)
			elif type == 'boolean':
				widget = BooleanWidget(label = label,
					label_msgid = label,
					description = description,
					description_msgid = description,
					#visible = {'edit':'visible', 'view':'invisible'},
					i18n_domain = I18N_DOMAIN,)
				result.append(BooleanField(field,widget = widget,),)
			else:
				widget = TextAreaWidget(label = label,
					label_msgid = label,
					description = description,
					description_msgid = description,
					#visible = {'edit':'visible', 'view':'invisible'},
					rows = 12,
					i18n_domain = I18N_DOMAIN,)
				result.append(TextField(field,widget = widget,),)
		return result

registerATCT(ECAutoAssessmentTask,PRODUCT_NAME)
