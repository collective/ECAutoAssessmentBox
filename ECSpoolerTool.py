# -*- coding: utf-8 -*-
# $Id$
#
# Copyright (c) 2007 Otto-von-Guericke-Universität Magdeburg
#
# This file is part of ECAutoAssessmentBox.
#
# ECAutoAssessmentBox is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# ECAutoAssessmentBox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ECAutoAssessmentBox; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
from random import LOG4


import os, sys
import socket, xmlrpclib
import traceback

from Products.CMFPlone.utils import log_exc, log

from AccessControl import ClassSecurityInfo, ModuleSecurityInfo
from Globals import InitializeClass
from OFS.Folder import Folder

from Products.Archetypes.public import *

from Products.CMFCore.permissions import View, ManagePortal
from Products.CMFCore.utils import UniqueObject

# local imports
from Products.ECAutoAssessmentBox.config import *


class ConnectionFailedException(Exception):
    """
    """
    pass

    
#class ECSpoolerTool(UniqueObject, SimpleItem):
class ECSpoolerTool(UniqueObject, Folder):
    """
    The ECSpoolerTool provides methods to communicate with 
    ECSpooler service.
    
    Connection values as well as selected backends are stored as 
    portal properties
    
    TODO:
     - in getBackendTestFields and getBackendInputFields use the cache
     - check if the version of a backend is compatible with the cached 
       version before using the cache
     - check methods' security
    """

    # set class security
    security = ClassSecurityInfo()
    security.declareObjectProtected(View)
    
    # set instance properties
    id = ECS_NAME
    portal_type = meta_type = ECS_META
    title = ECS_TITLE

    # manage options
    manage_options = (
        (Folder.manage_options[0],)
        + Folder.manage_options[2:]
        )

    # cache for backend values
    backendValueCache = {} 
    
    # spooler handle
    _spoolerHandle = None


    # -- constructor -----------------------------------------------------------
    def __init__(self):
        """
        """
        pass


    # -- methods ---------------------------------------------------------------
    #security.declarePublic('getStatus')
    def _getStatus(self, host=None, port=None, username=None, password=None):
        """
        Returns spooler status information
        """
        #log("Getting spooler status information")
        
        try:
            spooler = self._getSpoolerHandle(host, port)
            return spooler.getStatus(self._getAuth(username, password))

        except (socket.error, xmlrpclib.Fault), err:
            log_exc()
            pass


    #security.declarePrivate('_getAvailableBackends')
    def _getAvailableBackends(self, host=None, port=None, username=None, password=None):
        """
        Returns a dict with all backends currently registered to ECSpooler.
        """
        #log("Trying to get all available backends")
        
        try:
            spooler = self._getSpoolerHandle(host, port)
            return spooler.getBackends(self._getAuth(username, password))

        except (socket.error, xmlrpclib.Fault), err:
            log_exc()
            return {}


    security.declarePublic('getAvailableBackendsDL')
    def getAvailableBackendsDL(self):
        """
        Returns a display list of all (actually) available backends.
        """
        dl = DisplayList(())
        
        # get all available backends from spooler setup utily 
        backends = self._getAvailableBackends()
        
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
        log("manage_cacheBackends: reinit=%s" % reinit)
        
        if reinit:
            self.backendValueCache.clear()
        
        selectedBackends = self.portal_properties.ecspooler_properties.backends
        #log('ecspooler_properties.backends=%s' % selectedBackends)
        
        for backend in selectedBackends:
            self._cacheBackend(backend)


    security.declarePrivate('_cacheBackend')
    def _cacheBackend(self, backend):
        """
        Chaches all values for a backend.  Returns True if caching was ok, 
        otherwise False
        """
        #log("Caching backend '%s'" % backend)
        
        if not backend: 
            return False
        
        cache = self.backendValueCache
        
        try:
            status = None
            spooler = self._getSpoolerHandle()
            
            status = spooler.getBackendStatus(self._getAuth(), backend)
                
            if status and status[0]:
                cache[backend] = {}
                cache[backend]['name'] = status[1]['name']
                cache[backend]['version'] = status[1]['version']
                
                fields = spooler.getBackendInputFields(self._getAuth(), backend)
                if fields[0]:
                    cache[backend]['fields'] = fields[1]
                    
                tests = spooler.getBackendTestFields(self._getAuth(), backend)
                if tests[0]:
                    cache[backend]['tests'] = tests[1]

                log("Backend '%s' cached" % backend)

                return True

            else:
                return False

        except (socket.error, xmlrpclib.Fault), err:
            log_exc()
            return False
        #except Exception, e:
        #    log_exc()
        #    raise Exception(sys.exc_info()[0], e)


    security.declarePublic('getCachedBackends')
    def getCachedBackends(self):
        """
        Returns a list of backends which schema information are cached. 
        """
        #log("getCachedBackends")
        
        result = []
        
        availableBackends = self._getAvailableBackends().keys()
        
        for backend in self.backendValueCache.keys():
            try:
                result.append({'name': self.backendValueCache[backend]['name'],
                               'version': self.backendValueCache[backend]['version'],
                               'online': backend in availableBackends,
                               })
            except Exception, e:
                log_exc()
        
        return result


    security.declarePublic('setSelectedBackends')
    def setSelectedBackends(self, backends):
        """
        Sets the list of currently selected backends.
        """
        self.portal_properties.ecspooler_properties.backends = backends

    
    security.declarePublic('getSelectedBackends')
    def getSelectedBackends(self):
        """
        Returns a list of all backends selected for this site.
        """
        return self.portal_properties.ecspooler_properties.backends
        

    security.declarePublic('getSelectedBackendsDL')
    def getSelectedBackendsDL(self, withNone=True):
        """
        Returns a display list of all backends selected for this site.
        """
        dl = DisplayList(())
        
        if withNone:
            # set a value for none testing
            value = 'none'
            label = self.translate(msgid = 'label_no_backend', 
                                   domain = I18N_DOMAIN,
                                   default = 'None')
            dl.add(value, label)
        
        # add backends (they must be in the list of selected backends)
        selectedBackends = self.portal_properties.ecspooler_properties.backends
        
        for backend in selectedBackends:
            
            if backend:
                
                isCached = self.backendValueCache.has_key(backend)
                
                #log('1-xxx: %s : is chached: %s' % (backend, isCached))
                
                if not isCached:
                    isCached = self._cacheBackend(backend) 
                # end if
    
                #log('2-xxx: %s : is chached: %s' % (backend, isCached))

                if isCached:
                    dl.add(backend, '%s (%s)' % 
                           (self.backendValueCache[backend].get('name', '?'),
                            self.backendValueCache[backend].get('version', '?'))
                           )
                # end if
            # end if
             
        return dl

    
    security.declarePublic('getBackendInputFields')
    def getBackendInputFields(self, backend):
        """
        Returns a dict with all fields for this backend.
        """
        log("getBackendInputFields: %s" % backend)
        
        # look if the backend is available
        if backend in self._getAvailableBackends():
            # is this backend already cached?
            if not self.backendValueCache.has_key(backend):
                # not in cache -> get the fields from spooler
                try:
                    spooler = self._getSpoolerHandle()
                    fields = spooler.getBackendInputFields(self._getAuth(), 
                                                           backend)

                    if fields[0]:
                        # check if the backend is already cached
                        if not self.backendValueCache.has_key(backend):
                            self.backendValueCache[backend] = {}
        
                        # chache fields for this backend
                        self.backendValueCache[backend]['fields'] = fields[1]

                except (socket.error, xmlrpclib.Fault), err:
                    #log('%s' % err)
                    pass

        if self.backendValueCache.has_key(backend):
            return self.backendValueCache[backend]['fields']
        else:
            return {}


    security.declarePublic('getBackendTestFields')
    def getBackendTestFields(self, backend):
        """
        Returns a dict with test specifiactions for this backend.
        """
        log("getBackendTestFields: %s" % backend)

        # look if the backend is available
        if backend in self._getAvailableBackends():
            # is this backend already cached?
            if not self.backendValueCache.has_key(backend):
                # not in cache -> get the fields from spooler
                try:
                    spooler = self._getSpoolerHandle()
                    tests = spooler.getBackendTestFields(self._getAuth(), 
                                                         backend)

                    if tests[0]:
                        if not self.backendValueCache.has_key(backend):
                            self.backendValueCache[backend] = {}
        
                        self.backendValueCache[backend]['tests'] = tests[1]
        
                except (socket.error, xmlrpclib.Fault), err:
                    #log('%s' % err)
                    pass
            
        if self.backendValueCache.has_key(backend):
            return self.backendValueCache[backend]['tests']
        else:
            return {}


    security.declareProtected(edit_permission, 'test')
    def test(self, host=None, port=None, username=None, password=None):
        """
        Tests the connection to the spooler server.
        
        @return success or fail message string
        """
        status = self._getStatus(host, port, username, password)

        if status:
            # get backends
            backends = self._getAvailableBackends(host, port, username, password)
        
            bList = []
            [bList.append('%s (%s)' % (backends[key].get('name', 'xxx'), 
                                     backends[key].get('version', 'x.x'))) 
             for key in backends]

            return '[%s]' % ', '.join(bList)


    security.declarePublic('appendJob')
    #def appendJob(self, backend, input, **kwargs):
    def appendJob(self, backend, submission, inputFields, tests):
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
        
        #except AssertionError, aerr:
        except Exception, e:
            log_exc()
            return (-1, 'Internal error: %s: %s' % (sys.exc_info()[0], e))
    
    
    security.declarePublic('getResult')
    def getResult(self, jobId):
        """
        Returns the result for a check job with the given job id.
        """
        handle = self._getSpoolerHandle()
        username = self.portal_properties.ecspooler_properties.username
        password = self.portal_properties.ecspooler_properties.password

        AUTH = {'username':username, 'password':password}

        return handle.getResult(AUTH, jobId)
    

    security.declarePublic('refreshSpoolerHandle')
    def refreshSpoolerHandle(self):
        self._spoolerHandle = self._getSpoolerHandle()

    
    security.declarePrivate('_getSpoolerHandle')
    def _getSpoolerHandle(self, host=None, port=None):
        """
        Returns a handle to the spooler.
        """
        if not host:
            #self.host
            host = self.portal_properties.ecspooler_properties.host or 'localhost'
        
        if not port:
            #self.port
            port = self.portal_properties.ecspooler_properties.port or 5050
        
        assert (host != None) and (len(host) != ''), \
            "Host is required and must not be empty."
        assert (port != None) and (type(port) == int), \
            "Port is required and must be an integer."
            
        log("Getting spooler handle: http://%s:%d" % (host, port))

        #try:
        #log('xmlrpclib.Server("http://%s:%d")' % (host, port), severity=DEBUG)
        return xmlrpclib.ServerProxy("http://%s:%d" % (host, port))

        #except (socket.error, xmlrpclib.Fault), err:
        #except Exception, e:
        #    # FIXME: could not connect to server -> return a error message
        #    return None


    security.declarePrivate('_getAuth')
    def _getAuth(self, username=None, password=None):
        """
        """
        if not username:
            #self.username
            username = self.portal_properties.ecspooler_properties.username or ''
        
        if not password:
            #self.password
            password = self.portal_properties.ecspooler_properties.password or ''

        return {'username':username, 'password':password}

# initalize the tool
InitializeClass(ECSpoolerTool)
