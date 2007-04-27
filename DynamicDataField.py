# -*- coding: utf-8 -*-
# $Id$
#
# Copyright (c) 2007 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECAutoAssessmentBox.

# Python imports
from types import DictionaryType, StringType, UnicodeType, ListType

# Zope imports
from AccessControl import ClassSecurityInfo

# Plone imports
from Products.Archetypes.public import *
from Products.Archetypes.utils import mapply
from Products.Archetypes.Field import ObjectField, registerField, encode, decode

from Products.CMFPlone.utils import log_exc, log

# Local product imports
from Products.ECAutoAssessmentBox import DynamicDataWidget

class DynamicDataField(ObjectField):
    """ A dynamic field with undefined number of other fields

    DynamicDataField provides an user fillable list of field with 
    undefined number of fields.

    Data is maintained internally:
        - DynamicDataField.value is a list
        - Each list item is a dictionary using field names as a key

    DynamicDataField properties:
        - searchable:
            - If true all the contents of the DynamicDataField is concatenated
              to searchable text and given to text indexer
        - fields
            - List of dictionaries with field information, e.g., label or descr
        - widget:
            - must be DynamicDataWidget
    """
    
    #__implements__ = (ObjectField.__implements__, IDataGridField,)
    __implements__ = (ObjectField.__implements__,)

    _properties = ObjectField._properties.copy()
    _properties.update({
        'type' : 'dynamicdata',
        'mode' : 'rw',
        'default' : ({}),
        'widget' : DynamicDataWidget,
        'fields' : [],
        })

    security = ClassSecurityInfo()


    def __init__(self, name=None, **kwargs):
        """ Create DynamicDataField instance
        """

        # call super constructor
        ObjectField.__init__(self, name, **kwargs)

    security.declarePublic('fieldVocabulary')
    def fieldVocabulary(self, content_instance=None):
        """
        Returns a list of Field objects. Using self.fields as source.

        1) Static list
           - is already a list of fields

        2) Dynamic list:
           - precondition: a content_instance is given.
           - has to return a list of fields
           - fields is a string and if a method with the name of 
             the string exists it will be called
        """

        value = self.fields
        if not isinstance(value, DictionaryType):

            if content_instance is not None and type(value) in [StringType, UnicodeType]:
                # Dynamic vocabulary by method on class
                method = getattr(content_instance, value, None)
                if method and callable(method):
                    args = []
                    kw = {'content_instance' : content_instance,
                          'field' : self}
                    value = mapply(method, *args, **kw)

            else:
                log('Unhandled type in fields')
                log(value)

        return value


    security.declarePrivate('set')
    def set(self, instance, value, **kwargs):
        """
        """
        __traceback_info__ = value, type(value)
        
        if len(value) == 1:
            value = value[0]
        else:
            value = {}
            
        #log('setxxx: %s' % value)

        # fill in data
        ObjectField.set(self, instance, value, **kwargs)


    security.declarePrivate('get')
    def get(self, instance, **kwargs):
        """ Return DynamicDataField value

        Value is a list object of rows.

        If parameter mimetype == 'text/plain' is passed,
        a string containing all cell values concatenated together is returned.
        This is for site indexing services (DynamicDataField.searchable = true).
        """

        if(kwargs.has_key('mimetype') and kwargs['mimetype'] == 'text/plain'):
            # Data is returned for text indexing
            # Concatenate all cell values
            buffer = StringIO.StringIO()

            value = ObjectField.get(self, instance, **kwargs) or {}
            for item in value:
                buffer.write(value.get(item, ''))
                # separate the last word of a cell
                # and the first of the next cell
                buffer.write(' ')

            return encode(buffer.getvalue(), instance, **kwargs)

        else:
            # Return list containing all encoded rows
            value = ObjectField.get(self, instance, **kwargs) or {}
            data = encode(value, instance, **kwargs)
            #log('getxxx: %s' % data)
            
            #if type(data) != DictionaryType:
            #    data = {}
            
            return data
            
#            data = [encode(v, instance, **kwargs) for v in value]
#            log('getxxx: %s' % tuple(data))
#            return tuple(data)

    security.declarePrivate('getRaw')
    def getRaw(self, instance, **kwargs):
        return self.get(instance, **kwargs)

    security.declarePublic('get_size')
    def get_size(self, instance):
        """Get size of the stored data used for get_size in BaseObject
        """
        size=0
        for line in self.get(instance):
            size+=len(str(line))
        return size
        
        
registerField(DynamicDataField,
              title='DynamicDataField',
              description=('Used for storing a undefined number of fields'))
