# -*- coding: utf-8 -*-
# $Id$
#
# Copyright (c) 2006-2010 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECAutoAssessmentBox.
#
__author__ = """Mario Amelung <mario.amelung@gmx.de>"""
__docformat__ = 'plaintext'
__version__   = '$Revision: 1332 $'

import logging

from datetime import datetime

from Acquisition import aq_inner
from Acquisition import Explicit

from zope.component import adapts
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

from plone.app.kss.plonekssview import PloneKSSView

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from kss.core import KSSView, kssaction

logger = logging.getLogger('ECAutoAssessmentBox')

from Products.ECAutoAssessmentBox import ECMessageFactory as _

class BackendForm(Explicit):
    """
    """
    adapts(Interface, IDefaultBrowserLayer, IBrowserView)

    def __init__(self, context, request, view):
        """
        """
        #logger.info('request: %s' % request)
        #logger.info('xxx: backend: %s' % hasattr(request, 'backend'))
        
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

    logger.info("Processing 'BackendForm'")
    render = ViewPageTemplateFile("fieldset_backend.pt")


class Refresh(PloneKSSView):
    """
    """
    
    @kssaction
    def refresh_fieldset_backend(self, backend):
        """
        """
        logger.info("Processing 'refresh_fieldset_backend'")
        #logger.info(ViewPageTemplateFile("hello_world.pt"))
        
        context = aq_inner(self.context)

        core_commands = self.getCommandSet('core')
        zope_commands = self.getCommandSet('zope')
        plone_commands = self.getCommandSet('plone')

        #plone_utils = getToolByName(self.context, 'plone_utils')

        # set new backend
        logger.info('context: %s' % repr(context))
        context.tmpBackend = backend;

        selector = core_commands.getHtmlIdSelector('fieldsetBackend')
        #zope_commands.refreshProvider('#fieldsetBackend', name='ec.backend_form')
        zope_commands.refreshProvider(selector, name='ecaab.backend_form')
        #core_commands.replaceHTML(selector, '<fieldset tal:define="fieldsetid string:backend;sole_fieldset python:False"<div>Hello world!</div></fieldset>')
                
        plone_commands.issuePortalMessage((u'Backend changed to %s' % backend), msgtype='info')
