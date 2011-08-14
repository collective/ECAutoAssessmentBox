# -*- coding: utf-8 -*-
# $Id$
#
# Copyright (c) 2006-2011 Otto-von-Guericke-UniversitŠt Magdeburg
#
# This file is part of ECAutoAssessmentBox.
#
__author__ = """Mario Amelung <mario.amelung@gmx.de>"""
__docformat__ = 'plaintext'

from Acquisition import aq_inner
from Acquisition import Explicit

from zope.component import adapts
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.kss.plonekssview import PloneKSSView
from kss.core import KSSView
from kss.core import kssaction

from Products.ECAutoAssessmentBox import ECMessageFactory as _
from Products.ECAutoAssessmentBox import LOG

class FieldsetBackendInput(Explicit):
    """
    """
    adapts(Interface, IDefaultBrowserLayer, IBrowserView)

    def __init__(self, context, request, view):
        """
        """
        #LOG.info('xdebug: request: %s' % request)
        #LOG.info('xdebug: backend: %s' % hasattr(request, 'backend'))
        
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.backend = request.backend
        #planned = self.context.restrictedTraverse('@@planned-iterations')
        #self.projectlist = planned.projectlist()
        #self.total = planned.total()
        self.portal = getToolByName(context, 'portal_url').getPortalObject()
        
        if hasattr(request, 'errors'):
            self.errors = request.errors
        else:
            self.errors = {}

    def update(self):
        pass

    #LOG.info("xdebug: Processing 'FieldsetBackendInput'")
    render = ViewPageTemplateFile("fieldset_backend_input.pt")


class SelectBackendTests(Explicit):
    """
    """
    adapts(Interface, IDefaultBrowserLayer, IBrowserView)

    def __init__(self, context, request, view):
        """
        """
        #LOG.info('xdebug: request: %s' % request)
        #LOG.info('xdebug: backend: %s' % hasattr(request, 'backend'))
        
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.backend = request.backend
        #planned = self.context.restrictedTraverse('@@planned-iterations')
        #self.projectlist = planned.projectlist()
        #self.total = planned.total()
        self.portal = getToolByName(context, 'portal_url').getPortalObject()
        
        if hasattr(request, 'errors'):
            self.errors = request.errors
        else:
            self.errors = {}

    def update(self):
        pass

    #LOG.info("xdebug: Processing 'SelectBackendTests'")
    render = ViewPageTemplateFile("select_backend_tests.pt")

class Refresh(PloneKSSView):
    """
    """
    
    @kssaction
    def refresh_fieldset_backend(self, backend):
        """
        """
        #LOG.info("xdebug: Processing 'refresh_fieldset_backend'")
        #LOG.info("xdebug: Selected backend is '%s'" % backend)
        
        context = aq_inner(self.context)

        core_commands = self.getCommandSet('core')
        zope_commands = self.getCommandSet('zope')
        plone_commands = self.getCommandSet('plone')

        #plone_utils = getToolByName(self.context, 'plone_utils')

        # set new backend
        #LOG.info('xdebug: context: %s' % repr(context))
        context.kssBackend = backend;

        # refresh backend tests selection
        selector = core_commands.getHtmlIdSelector("archetypes-fieldname-tests")
        zope_commands.refreshProvider(selector, name='ecaab.select_backend_tests')
        
        
        # refresh backend input fields
        selector = core_commands.getHtmlIdSelector("fieldset-backend-data")
        zope_commands.refreshProvider(selector, name='ecaab.fieldset_backend_input')
                
        #plone_commands.issuePortalMessage((u'Backend changed to %s' % backend), msgtype='info')
