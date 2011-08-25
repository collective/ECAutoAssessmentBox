# -*- coding: utf-8 -*-
# $Id$
#
# Copyright (c) 2006-2011 Otto-von-Guericke-UniversitŠt Magdeburg
#
# This file is part of ECAutoAssessmentBox.
#
__author__ = """Mario Amelung <mario.amelung@gmx.de>"""
__docformat__ = 'plaintext'

# Python imports
#from types import DictType, FileType, StringType, UnicodeType

# Zope imports
from AccessControl import ClassSecurityInfo
#from Acquisition import aq_base, aq_parent

# Plone imports
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget
#from Products.Archetypes.debug import log
#from Products.Archetypes.utils import className, unique, capitalize
#from Products.CMFCore.utils import getToolByName
#from Products.CMFCore.Expression import Expression, createExprContext
#from Products.generator.widget import macrowidget

# Local imports
#from Column import Column


class DynamicDataWidget(TypesWidget):
    """ Render a data table with user addable rows

        Properties:
          - columns:
            - Dictionary of "column id" : Column instance mappings
                - Column instance:
                    - title: user friendly name
                - SelectColumn instance:
                    - title: user friendly name
                    - vocabulary: vocabulary function for used to get DisplayList for dropdown
    """

    _properties = TypesWidget._properties.copy()

    _properties.update({
        'macro' : "widget_dynamic_data",
        'helper_js': ('widget_dynamic_data.js',),
        'fields' : {}, # Sequence of Column instances
        })


    security = ClassSecurityInfo()

#    security.declarePublic('getColumnLabels')
#    def getColumnLabels(self, field):
#        """ Get user friendly names of all columns """
#
#        columnDefinitions = getattr(self, 'columns', {})
#        
#        if len(columnDefinitions) == 0:
#            # old way of getting column names
#            columnNames = getattr(self, 'column_names', [])
#            if columnNames:
#                return columnNames
#            else:
#                return field.getColumnIds()
#
#
#        names = []
#
#        for id in field.getColumnIds():
#            # Warn AT developer about his/her mistake
#            if not id in columnDefinitions:
#                raise AttributeError, "DynamicDataWidget missing column definition for " + id + " in field " + field.getName()
#
#            col = self.columns[id]
#            names.append(col.getLabel())
#
#        return names
#
#    security.declarePublic('getColumnDefinition')
#    def getColumnDefinition(self, field, id):
#        """ Return Column instance for column id """
#
#        if id in getattr(self, 'columns', {}).keys():
#            return self.columns[id].__of__(self)
#
#        # Backwards compatability/shortcut
#        if id in field.columns:
#            label = id
#            columnNames = getattr(self, 'column_names', None)
#            if columnNames and len(columnNames) == len(field.columns):
#                idx = list(field.columns).index(id)
#                label = columnNames[idx]
#                
#            return Column(label).__of__(self)
#
#        raise KeyError, "Tried to look up missing column definition for: " + str(id)
#
#    def getUserFriendlySelectionItem(self, context, item, vocab):
#        """Look up the given item in the vocab and return the value, translated
#        if necessary. Return an empty string if item is empty or None.
#        """
#        if item == None or item == '':
#            return ""
#        return context.translate(vocab.getMsgId(item), default=vocab.getValue(item))

__all__ = ('DynamicDataWidget')

registerWidget(DynamicDataWidget,
               title='Dynamic Data',
               description=('A list of a undefined number of fields'),
               used_for=('Products.ECAutoAssessmentBox.content.DynamicDataField',)
               )

