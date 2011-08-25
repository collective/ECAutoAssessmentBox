# -*- coding: utf-8 -*-
# $Id$
#
# Copyright (c) 2006-2011 Otto-von-Guericke-UniversitŠt Magdeburg
#
# This file is part of ECAutoAssessmentBox.
#
from docutils.nodes import status
__author__ = """Mario Amelung <mario.amelung@gmx.de>"""
__docformat__ = 'plaintext'

import sys
import socket
import xmlrpclib
import interfaces

#from xml.parsers.expat import ExpatError

from zope.interface import implements

from AccessControl import ClassSecurityInfo

from Products.Archetypes.atapi import Schema, BaseSchema, registerType
from Products.Archetypes.atapi import BaseContent, DisplayList

from Products.Archetypes.debug import log_exc

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore import permissions

from Products.ECAutoAssessmentBox import config
from Products.ECAutoAssessmentBox import LOG
from Products.ECAutoAssessmentBox import ECMessageFactory as _


ECSpoolerTool_schema = BaseSchema.copy()

# ID for the virtual non-backend
BACKEND_NONE = 'None'


class ConnectionFailedException(Exception):
    """
    """
    pass


class ECSpoolerTool(UniqueObject, BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IECSpoolerTool)

    plone_tool = True
    meta_type  = config.ECS_META

    schema = ECSpoolerTool_schema
    #_at_rename_after_creation = False

    # cache for backend values
    backendValueCache = {} 
    # spooler handle
    _spoolerHandle = None
    

    def __init__(self, id=None):
        """Tool-constructors have no id argument, the id is fixed
        """
        BaseContent.__init__(self, config.ECS_NAME)
        self.setTitle("")


    def at_post_edit_script(self):
        """Tool should not appear in portal_catalog
        """
        self.unindexObject()


    # -- Methods --------------------------------------------------------------
    
    #security.declarePublic('getStatus')
    def _getStatus(self, host=None, port=None, username=None, password=None):
        """
        Returns spooler status information
        """
        LOG.debug("Requesting spooler status information")

        try:
            spooler = self._getSpoolerHandle(host, port)
            LOG.debug("%s" % repr(spooler))
        
            return spooler.getStatus(self._getAuth(username, password))

        except xmlrpclib.Fault, e:
            LOG.warn("%s" % e)
        except socket.error, e:
            LOG.warn("%s" % e)

        return None
    

    #security.declarePrivate('_getAvailableBackends')
    def _getAvailableBackends(self, host=None, port=None, username=None, password=None):
        """Returns a dict with all backends currently registered and 
        available by ECSpooler.
        """
        LOG.debug("Trying to get available backends from...")
        
        try:
            spooler = self._getSpoolerHandle(host, port)
            #LOG.debug("%s" % repr(spooler))

            return spooler.getBackends(self._getAuth(username, password))

        except xmlrpclib.Fault, e:
            LOG.warn("%s" % e)
        except socket.error, e:
            LOG.warn("%s" % e)

        return {}


    security.declarePublic('getAvailableBackendsDL')
    def getAvailableBackendsDL(self):
        """
        Returns a display list of all (actually) available backends.
        """
        #LOG.debug("xdebug: getAvailableBackendsDL")

        dl = DisplayList(())
        
        # get all available backends from spooler setup utily 
        backends = self._getAvailableBackends()
        
        #LOG.debug('xdebug: backends: ' + repr(backends))
        
        for key in backends.keys():
            id = key
            label = '%s (%s)' % (backends[key].get('name', '?'), 
                                 backends[key].get('version', '?'))
            
            dl.add(id, label)
             
        return dl

   
    security.declarePublic('manage_cacheBackends')
    def manage_cacheBackends(self, reinit=False):
        """
        Values for all currently selected backends will be chached.
        """
        #LOG.debug("xdebug: manage_cacheBackends: reinit=%s" % reinit)
        
        if reinit:
            self.backendValueCache.clear()
        
        for backend in self.getSelectedBackends():
            self._cacheBackend(backend)


    security.declarePrivate('_cacheBackend')
    def _cacheBackend(self, backend):
        """ Caches all values for a given backend.  Returns True if 
        the caching procedure was successful, otherwise False.
        """
        #LOG.debug("xdebug: Caching backend '%s'" % backend)
        
        if not backend: 
            return False
        
        cache = self.backendValueCache
        
        try:
            status = None
            spooler = self._getSpoolerHandle()
            
            status = spooler.getBackendStatus(self._getAuth(), backend)
                
            if status:
                if status[0] > 0:
                    cache[backend] = {}
                    cache[backend]['name'] = status[1]['name']
                    cache[backend]['version'] = status[1]['version']
                    
                    fields = spooler.getBackendInputFields(self._getAuth(), backend)
                    if fields[0]:
                        cache[backend]['fields'] = fields[1]
                        
                    tests = spooler.getBackendTestFields(self._getAuth(), backend)
                    if tests[0]:
                        cache[backend]['tests'] = tests[1]
    
                    #LOG.debug("xdebug: Backend '%s' successfully cached" % backend)
    
                    return True
                
                elif status[0] < 0:
                    LOG.warn('Error while getting backend status: %s, %s' % (status[0], status[1]))
            else:
                LOG.warn('Error while getting backend status: status is %s' % (status))

        except xmlrpclib.Fault, e:
            LOG.warn("%s" % e)
        except socket.error, e:
            LOG.warn("%s" % e)

        return False

    security.declarePublic('getCachedBackends')
    def getCachedBackends(self):
        """Returns a list of backends which schema information 
        is in the local cache. 
        """
        #LOG.debug("xdebug: Getting cached backends")
        
        result = []
        
        #availableBackends = self._getAvailableBackends().keys()
        
        for backend in self.backendValueCache.keys():
            try:
                result.append({'name': self.backendValueCache[backend]['name'],
                               'version': self.backendValueCache[backend]['version'],
                               #'online': backend in availableBackends,
                               })
            except Exception, e:
                LOG.warn("%s" % e)

        return None
        
        return result


    security.declarePublic('setSelectedBackends')
    def setSelectedBackends(self, backends):
        """
        Sets the list of currently selected backends.
        """
        self.portal_properties.ecaab_properties.backends = backends

    
    security.declarePublic('getSelectedBackends')
    def getSelectedBackends(self):
        """Returns a list of all backends selected for this site.
        """
        return self.portal_properties.ecaab_properties.backends
        

    security.declarePublic('getSelectedBackendsDL')
    def getSelectedBackendsDL(self, withNone=True):
        """Returns a display list of all backends selected for this site.
        """
        #LOG.debug("Getting all selected backends as Archetypes.utils.DisplayList...")

        dl = DisplayList(())
        
        if withNone:
            # set a value for no testing
            value = BACKEND_NONE
            dl.add(value, '----')
        
        for backend in self.getSelectedBackends():

            if backend != None:
                isCached = self.backendValueCache.has_key(backend)
                #LOG.debug("xdebug: backend '%s' is cached: %s" % (backend, isCached))
                
                if not isCached:
                    isCached = self._cacheBackend(backend) 
                    #LOG.debug("xdebug: backend '%s' is cached: %s" % (backend, isCached))
                # end if

                if isCached:
                    #LOG.debug("xdebug: Adding backend '%s' to display list" % backend)
                    dl.add(backend, '%s (%s)' % 
                           (self.backendValueCache[backend].get('name', '?'),
                            self.backendValueCache[backend].get('version', '?'))
                           )
                else:
                    LOG.warn("Cannot add backend '%s' to display list "
                             "because it is not cached" % backend)
                # end if
            # end if
        # end for
             
        return dl

    
    security.declarePublic('getBackendInputFields')
    def getBackendInputFields(self, backend):
        """Returns a dict with all input fields for this backend.
        """
        
        result = {}
        
        if backend != BACKEND_NONE:
            
            #LOG.debug("Loading backend input fields for '%s'" % backend)
            
            # look if the backend is available
            #if backend in self._getAvailableBackends():
    
            # is this backend already cached?
            if not self.backendValueCache.has_key(backend):
                # not in cache -> try getting field information directly from 
                # spooler and cache them
                #LOG.debug("xdebug: Input fields for backend '%s' are not cached" % (backend))
                self._cacheBackend(backend)
            # end if
    
            # backend input fields should be cached now
            if self.backendValueCache.has_key(backend):
                result = self.backendValueCache[backend]['fields']

        return result


    security.declarePublic('getBackendTestFields')
    def getBackendTestFields(self, backend):
        """Returns a dict with test specifiactions for this backend.
        """

        result = {}
        
        if backend != BACKEND_NONE:
            
            #LOG.debug("Loading backend test fields for '%s'" % backend)
    
            # look if the backend is available
            #if backend in self._getAvailableBackends():
    
            # is this backend already cached?
            if not self.backendValueCache.has_key(backend):
                # not in cache -> try getting field information directly from 
                # spooler and cache them
                #LOG.debug("xdebug: Test fields for backend '%s' are not cached" % (backend))
                self._cacheBackend(backend)
            # end if
                
            # backend test fields should be cached now
            if self.backendValueCache.has_key(backend):
                result = self.backendValueCache[backend]['tests']

        return result


    security.declareProtected(permissions.ModifyPortalContent, 'test')
    def test(self, host=None, port=None, username=None, password=None):
        """
        Tests the connection to the spooler server.
        
        @return success or fail message string
        """
        LOG.debug("Testing spooler connection")

        status = self._getStatus(host, port, username, password)
        
        if status:
            if status[0] > 0:
                # get backends
                backends = self._getAvailableBackends(host, port, username, password)
            
                bIdList = []
                [bIdList.append(key) for key in backends]
    
                bNameList = []
                [bNameList.append('%s (%s)' % (backends[key].get('name', 'xxx'), 
                                         backends[key].get('version', 'x.x'))) 
                  for key in backends]
    
                return bIdList, '[%s]' % ', '.join(bNameList)

            elif status[0] < 0:
                return None, status[1]
        else:
            return None, "Service not responding (%s:%s)" % (host, port)


    security.declarePublic('appendJob')
    #def appendJob(self, backend, input, **kwargs):
    def appendJob(self, backend, submission, inputFields, tests, retry=True):
        """
        Adds a job to the spooler server.
        """

        try:
            spooler = self._getSpoolerHandle()

            data = {}
            # set the backend
            data['backend'] = backend
            # set student solution
            data['submission'] = submission
            # set tests
            data['tests'] = tests
            # set input fields
            data.update(inputFields)

            result = spooler.appendJob(self._getAuth(), data)

            # FIXME: do some testing with this result
            assert result[0], result[1]
            
            return result
        
        except xmlrpclib.Fault, ef:
            LOG.warn('%s: %s' % (sys.exc_info()[0], ef))
            
            if retry:
                # take care of hexadecimal Unicode escape sequences
                submission = submission.decode('unicode_escape')
                # retry appending this submission 
                return self.appendJob(backend, submission, inputFields, tests, False)

        except Exception, e:
            log_exc()
            return (-1, 'Internal error: %s: %s' % (sys.exc_info()[0], e))
    
    
    security.declarePublic('getResult')
    def getResult(self, jobId):
        """
        Returns the result for a check job with the given job id.
        """
        handle = self._getSpoolerHandle()
        username = self.portal_properties.ecaab_properties.username
        password = self.portal_properties.ecaab_properties.password

        AUTH = {'username':username, 'password':password}

        return handle.getResult(AUTH, jobId)
    

    security.declarePublic('refreshSpoolerHandle')
    def refreshSpoolerHandle(self):
        """
        """
        self._spoolerHandle = self._getSpoolerHandle()

    
    security.declarePrivate('_getSpoolerHandle')
    def _getSpoolerHandle(self, host=None, port=None):
        """
        Returns a handle to the spooler.
        """
        if not host:
            #self.host
            host = self.portal_properties.ecaab_properties.host# or 'localhost'
        
        if not port:
            #self.port
            port = self.portal_properties.ecaab_properties.port# or 5050
        
        assert (host != None) and (len(host) != ''), \
            "Host is required and must not be empty."
        assert (port != None) and (type(port) == int), \
            "Port is required and must be an integer."
            
        LOG.debug("Spooler handle: http://%s:%d" % (host, port))
        return xmlrpclib.ServerProxy("http://%s:%d" % (host, port))


    security.declarePrivate('_getAuth')
    def _getAuth(self, username=None, password=None):
        """
        """
        if not username:
            #self.username
            username = self.portal_properties.ecaab_properties.username or ''
        
        if not password:
            #self.password
            password = self.portal_properties.ecaab_properties.password or ''

        return {'username':username, 'password':password}


registerType(ECSpoolerTool, config.PROJECTNAME)
