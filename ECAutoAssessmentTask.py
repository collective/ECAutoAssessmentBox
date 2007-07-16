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
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import registerATCT,updateAliases,updateActions
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.folder import ATFolderSchema,ATFolder

from Products.ECAutoAssessmentBox.PlainTextField import PlainTextField
from Products.ECAutoAssessmentBox.config import *



ECAutoAssessmentTaskSchema = ATFolderSchema.copy() + Schema((
	TextField(
		'assignment_text',
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
	PlainTextField(
		'answerTemplate',
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
#    StringField(
#        'backend',
#        required = True,
#        vocabulary = 'getBackendDisplayList',
#        widget = SelectionWidget(
#            modes=('edit'),
#            label='Test backend',
#            label_msgid='label_backend',
#            description='Select a test backend.',
#            description_msgid='help_backend',
#            i18n_domain=I18N_DOMAIN,
#        ),
#        read_permission = permissions.ModifyPortalContent,
#    ),
#    BooleanField(
#        'autoAccept',
#        default = False,
#        #required = True,
#        widget = BooleanWidget(
#            label = 'Automatically accept assignments',
#            label_msgid = 'label_auto_accept',
#            description = 'If selected, an assignment which passes all tests will be automatically accepted.',
#            description_msgid = 'help_auto_accept',
#            i18n_domain = I18N_DOMAIN,
#        ),
#        schemata = 'backend',
#        read_permission = permissions.ModifyPortalContent,
#    ),
#    StringField(
#        'tests',
#        #required = True,
#        vocabulary = '_getTestsDisplayList',
#        widget = MultiSelectionWidget(
#            modes=('edit'),
#            label='Tests',
#            label_msgid='label_tests',
#            description='Select one or more tests.',
#            description_msgid='help_tests',
#            i18n_domain=I18N_DOMAIN,
#        ),
#        schemata = 'backend',
#        read_permission = permissions.ModifyPortalContent,
#    ),
))

finalizeATCTSchema(ECAutoAssessmentTaskSchema)



class ECAutoAssessmentTask(ATFolder):
	"""Defines the task for an auto assessment box.
	"""

	portal_type = meta_type = ECAAT_META
	archetype_name = ECAAT_NAME
	content_icon = 'ecaat.png'
	schema = ECAutoAssessmentTaskSchema
	typeDescription = 'Allows the creation of online assignments.'
	typeDescMsgID = 'description_edit_ecaat'

	_at_rename_after_creation = True
	__implements__ = ATFolder.__implements__

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


registerATCT(ECAutoAssessmentTask,PRODUCT_NAME)
