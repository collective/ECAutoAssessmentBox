# -*- coding: utf-8 -*-
# $Id: ecaabsettings.py 1584 2011-08-14 09:45:05Z amelung $
#
# Copyright (c) 2006-2011 Otto-von-Guericke-UniversitŠt Magdeburg
#
# This file is part of ECAutoAssessmentBox.
#
__author__ = """Mario Amelung <mario.amelung@gmx.de>"""
__docformat__ = 'plaintext'

#from Acquisition import aq_inner

from zope import event
from zope.app.component.hooks import getSite
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements, Interface
#from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent import ObjectModifiedEvent
#from zope.schema import Text
from zope.schema import TextLine
from zope.schema import List
from zope.schema import Int
from zope.schema import Password
#from zope.schema import Tuple
#from zope.schema import Choice

from plone.app.controlpanel.form import ControlPanelForm
#from plone.app.form.validators import null_validator
from plone.fieldsets.fieldsets import FormFieldsets

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
#from Products.CMFPlone.PropertiesTool import SimpleItemWithProperties

from Products.ECAutoAssessmentBox import ECMessageFactory as _
from Products.ECAutoAssessmentBox import config
from Products.ECAutoAssessmentBox import LOG

I18N_DOMAIN = 'eduComponents'

class IECAABControlPanelSpoolerSchema(Interface):
    """
    Spooler fieldset schema
    """

    host = TextLine(
            title=_(u"label_host", default=u"Host"),
            description=_(u"help_host",
                          default=u"The address of your spooler service (e. g., host.yourdomain.com)."),
            default=u'localhost',
            required=True)

    port = Int(
            title=_(u"label_port", default=u"Port"),
            description=_(u"help_port",
                          default=u"The port of your spooler service (e.g., 5050)."),
            default=5050,
            required=True)

    username = TextLine(
            title=_(u"label_username", default=u"Username"),
            description=_(u"help_username",
                          default=u"Username for authentication to your spooler service."),
            default = u'demo',
            required = True)

    password = Password(
            title=_(u"label_password", default=u"Password"),
            description =_(u"help_password", default=u"Password or authentication to your spooler service."),
            default = u'foobar',
            required = True)


class IECAABControlPanelBackendsSchema(Interface):
    """
    Backends fieldset schema
    """

    backends = List(title=_(u"Available backends"),
                    description=_(u"All backends currently available " 
                                   "for this site"),
                    value_type=TextLine(),
                    default=[],
                    readonly=True,
                    required=False)
    """
    backends = Tuple(title=_(u"Available backends"),
                     description=_(u"Available backends "
                                  "for for your site. "),
                     required=False,
                     missing_value=tuple(),
                     #default = (),
                     value_type = Choice(vocabulary="ecaab.vocabularies.backends"))
    """


class IECAABControlPanelSchema(IECAABControlPanelSpoolerSchema, IECAABControlPanelBackendsSchema):
    """
    Combined schema for the adapter lookup.
    """


class ECAABControlPanelAdapter(SchemaAdapterBase):

    implements(IECAABControlPanelSchema)
    #implements(IECAABControlPanelSpoolerSchema)
    adapts(IPloneSiteRoot)
    
    def __init__(self, context):
        super(ECAABControlPanelAdapter, self).__init__(context)
        self.portal = getSite()
        pprop = getToolByName(self.portal, 'portal_properties')
        self.context = pprop.ecaab_properties
        #self.encoding = pprop.site_properties.default_charset

    # base fieldset

    def get_host(self):
        return self.context.host

    def set_host(self, value):
        self.context._updateProperty('host', value)

    host = property(get_host, set_host)

    def get_port(self):
        return self.context.port

    def set_port(self, value):
        self.context._updateProperty('port', value)

    port = property(get_port, set_port)

    def get_username(self):
        return self.context.username

    def set_username(self, value):
        self.context._updateProperty('username', value)

    username = property(get_username, set_username)

    def get_password(self):
        return self.context.password

    def set_password(self, value):
        self.context._updateProperty('password', value)

    password = property(get_password, set_password)

    def get_backends(self):
        return self.context.backends

    def set_backends(self, value):
        self.context._updateProperty('backends', value)

    backends = property(get_backends, set_backends)
    

spooler_set = FormFieldsets(IECAABControlPanelSpoolerSchema)
spooler_set.id = 'ecaab_settings_spooler'
spooler_set.label = _(u"legend_ecspooler_details", default=u"Spooler connection settings")

backends_set = FormFieldsets(IECAABControlPanelBackendsSchema)
backends_set.id = 'ecaab_settings_backends'
backends_set.label = _(u"legend_backend_details", default=u"Available backends")
 
 
class ECAABControlPanel(ControlPanelForm):
    """
    """
    
    form_fields = FormFieldsets(spooler_set, backends_set)

    label = _(u"heading_ecspooler_setup", 
              default=u"Auto Assessment Box Settings")
    
    description = _(u"description_ecspooler_setup",
                    default=u"Lets you control which spooler service will be "
                             "used and which backends are available in your site.")
    
    form_name = _("ECAAB settings")


    @form.action(
        _(u'apply_ecaab_settings',
          default=u'Apply settings'),
        name=u'apply_ecaab_settings')
    def apply_ecaab_settings(self, action, data):
        """Save settings to portal properties and test this new settings.
        """
        
        msg = ""

        if form.applyChanges(
            self.context, self.form_fields, data, self.adapters):
            event.notify( ObjectModifiedEvent(self.context))
            #formatter = self.request.locale.dates.getFormatter('dateTime', 'medium')
        
            # read properties
            portal_props = getToolByName(getSite(), 'portal_properties')
            ecaab_props = portal_props.ecaab_properties
        
            host = ecaab_props.host
            port = int(ecaab_props.port)
            username = ecaab_props.username
            password = ecaab_props.password
            
        
            # get spooler tool
            ecs_tool = getToolByName(getSite(), 'ecaab_utils')
            # test connection without saving
            backendIds, msg = ecs_tool.test(host, port, username, password)
        
            if backendIds is not None:
                ecaab_props._updateProperty('backends', backendIds)
                
                msg = _(u'update_succeeded',
                        default=u'Your changes have been saved.  '
                                 'The following backends are available: %s. '
                                 %  msg)
            else:
                msg = _(u'test_failed',
                        default=u'%s' % msg)
                
        else:
            msg = _(u'no_changes', default=u'No changes')

        
        # set portal message
        self.context.plone_utils.addPortalMessage(msg)


    @form.action(
        _(u'reset_backend_cache',
          default=u'Reset backend cache'),
        name=u'reset_backend_cache')
    def reset_backend_cache(self, action, data):
        """
        Resets internal cache for backend information such as 
        input and test fields.
        """
        
        # get spooler tool
        ecs_tool = getToolByName(getSite(), 'ecaab_utils')
        # clear backend cache and re-init it
        ecs_tool.manage_cacheBackends(reinit=True)

        # set portal message
        msg = _(u'cache_reseted', default=u'Backend cache has been re-initialized.')
        self.context.plone_utils.addPortalMessage(msg)
