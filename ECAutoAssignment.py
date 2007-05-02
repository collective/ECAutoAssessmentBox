# -*- coding: utf-8 -*-
# $Id$
#
# Copyright (c) 2005 Otto-von-Guericke-University, Magdeburg
#
# This file is part of ECAutoAssessmentBox.
"""
TODO: 
"""
# Pythone imports
import sys, re, time
import xmlrpclib
import traceback

from types import BooleanType
from types import IntType

# Zope imports
from AccessControl import Unauthorized
from AccessControl.SecurityManagement import getSecurityManager, setSecurityManager, newSecurityManager

# Plone imports
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.utils import log_exc, log

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.CMFCore import CMFCorePermissions
from Products.ATContentTypes.content.base import updateActions, updateAliases, ATCTContent

# Other product imports

# Local product imports
from Products.ECAutoAssessmentBox.config import *
from Products.ECAssignmentBox.ECAssignment import ECAssignment

# set max wait time; after a maxium of 15 tries we will give up getting 
# any result from the spooler until this assignment will be accessed again
MAX_WAIT_TIME = 15
MAX_SLEEP_TIME = 1.2

# define schema
localSchema = Schema((
    # backendResultMessage
    TextField(
        'auto_feedback',
        searchable = True,
        widget = ComputedWidget(
            label = "Auto feedback",
            label_msgid = "label_auto_feedback",
            description = "The automatic feedback for this assignment.",
            description_msgid = "help_auto_feedback",
            i18n_domain = I18N_DOMAIN,
            macro = 'auto_feedback_widget',
        ),
    ),

    # backendResultValue
    StringField(
        'backendResultCode',
        #searchable = True,
        #accessor = 'getMappedBackendResultCode',
        widget=ComputedWidget(
            modes=('view'),
            label='Backend result code',
            label_msgid = "label_result_code",
            description = "The result code of the backend for this assignment.",
            description_msgid = 'help_result_code',
            i18n_domain = I18N_DOMAIN,
        )
    ),

    StringField(
        'jobId',
        searchable = False,
        widget=ComputedWidget(
            modes=('view'),
            label='Job id',
            label_msgid = "label_job_id",
            description = "The id of the spooler job for this assignment.",
            description_msgid = 'help_job_id',
            i18n_domain = I18N_DOMAIN,
        ),
    ),

))


class ECAutoAssignment(ECAssignment):
    """Submission to an auto assessment box."""

    __implements__ = (ECAssignment.__implements__,)
    security = ClassSecurityInfo()

    schema = ECAssignment.schema + localSchema
    portal_type = meta_type = ECAA_META
    archetype_name = ECAA_TITLE
    default_view   = 'ecaa_view'
    immediate_view = 'ecaa_view'


    # -- actions --------------------------------------------------------------
    aliases = updateAliases(ECAssignment, {
        'view': 'ecaa_view',
        #'grade': 'ecaa_grade',
        })


    # -- methods --------------------------------------------------------------
    security.declarePublic('getAutoFeedback')
    def getAutoFeedback(self):
        """
        Returns the message given by the test backend for this submission.  
        If there is no result we will try to get one from spooler/backend.
        
        @return: feedback message as String
        """
        if not self.auto_feedback:
            try:
                spooler = getToolByName(self, 'ecspooler_tool')
                assert spooler != None, "Spooler tool not installed."
            
                result = spooler.getResult(self.jobId)
                
                log('[%s] result: %s' % (self.getId(), repr(result)))
    
                if result.has_key(self.jobId):
                    self.setBackendResultCode(result[self.jobId].get('code'))
                    self.setAuto_feedback(result[self.jobId].get('value'))
                    
                    #self._autoAccept()
                    
                    # change workflow state if parent assignment box has auto 
                    # accept enabled.
                    if (self.aq_parent.getAutoAccept()) and (self.isSolved()):
                        self._changeWfState('accept', 
                                           "Automatically checked by '%s' and accepted." % backend)
                    else:
                        self._changeWfState('retract', 
                                           "Automatically checked by '%s'." % backend)
                    
            except Exception, e:
                log('Error: %s' % str(e))
            
        return self.getAuto_feedback()


    security.declarePublic('isSolved')
    def isSolved(self):
        """
        If backendResultCode is a Boolean True or False will be returned, 
        otherwise None.
        """
        
        if hasattr(self, 'backendResultCode'):

            resultValue = self.backendResultCode
        
            if type(resultValue) == BooleanType:
                return resultValue

        return None


    security.declarePrivate('_changeWfState')
    def _changeWfState(self, transition, comment=None):
        """
        Sets the workflow state of this assignment to state. Since unpriviliged
        users are not allowed to change workflow state we switch security
        context.
        
        @param transition
        @param comment
        """
        wftool = getToolByName(self, 'portal_workflow')
        # FIXME: we use the 1st workflow for this object, but there can be
        #        more workflows assigned to this object!
        wf = wftool.getWorkflowsFor(self)[0]
        #log('xxx: review_state: %s' % wf.getInfoFor(self, 'review_state', ''))
        
        REQUEST = self.REQUEST
        
        # because we switch security context, we have to remember the current user
        currentUser = getSecurityManager().getUser()
        # get user of parent object
        wrappedUser = self.aq_parent.getWrappedOwner() 
        
        #log('current user: %s' % currentUser)
        #log('wrapped user: %s' % wrappedUser)
        
        # set security context for the owner of the parent object (assignment box)
        newSecurityManager(REQUEST, wrappedUser) 

        #log('xxx: %s' % repr(wftool.getTransitionsFor(self, REQUEST=REQUEST)))
        #log('xxx: isActionSupported(%s): %s' % (transition, wf.isActionSupported(self, transition)))
        
        # do the workflow state change
        if wf.getInfoFor(self, 'review_state', '') != 'superseded':
            #try:
            if wf.isActionSupported(self, transition):
                if comment is None:
                    comment = 'State changed. [real user: %s]' % currentUser
                else:
                    # add the "real" user to comment
                    comment = comment + ' [real user: %s]' % currentUser
            
                wftool.doActionFor(self, transition, comment=comment)
            else:
                log('Unsupported workflow action %s for object %s.' % (repr(transition), repr(self)))
            
            #except Exception, e:
            #    log_exc(e)
            #    raise e

        # end if

        # return to the current users security context
        newSecurityManager(REQUEST, currentUser) 
        

    # -- overridden methods from ECAssignment ---------------------------------
    security.declarePublic('evaluate')
    def evaluate(self, parent, recheck=False):
        """
        Evaluates the student solution via ECSpooler.
        @see ECAssignment.evaluate
        
        @parent parent of this instance, naturally ECAutoAssessmentBox
        @return message string
        """
        result = 1;
        msgId = ''
        msgDefault = ''
        
        # get the selected backend in the parent box
        backend = parent.getBackend()
        
        if backend == 'manual':
            #return self.translate(
            #    msgid   = 'no_backend_given',
            #    domain  = I18N_DOMAIN,
            #    default = 'Automatic checking failed. No backend was specified.')

            # behave like a normal assginment box
            return ECAssignment.evaluate(self, parent)
        
        try:
            # get input fields needed by this backend
            inputFields = parent.getInputFields()
            # get selected tests provided by this backend
            tests = parent.getTests()

            # set student solution 
            studentSolution = self.getAsPlainText()
            
            if not studentSolution:
                # FIXME: translate error message
                raise Exception('Submission is not plain text.')
    
            self._changeWfState('review', 
                                "Queued for automatic checking by '%s'." % backend)
    
            spoolerWSI =  getToolByName(self, 'ecspooler_tool')
            assert spoolerWSI != None, "A valid portal ecspooler is required."
    
            # enqueue students' solution
            # TODO: rename sample_soution to model_solution
    
            job = spoolerWSI.appendJob(backend, studentSolution, 
                                       inputFields, tests)

            log('[%s] enqueue: %s' % (self.getId(), repr(job)))
            
            # validate job id?
            if job[0] == 0:
                # remember the job id and set inital values for feedback
                self.jobId = job[1]
                feedback = {}
                i = 0

                # reset feedback text
                self.auto_feedback = ''

                # wait until a feedback has been retrieved from the spooler
                # or max number of retries has been reached
                while (not feedback.has_key(self.jobId)) and (i < MAX_WAIT_TIME):
                    time.sleep(MAX_SLEEP_TIME)
                    feedback = spoolerWSI.getResult(self.jobId)
                    i += 1
                    
                if feedback.has_key(self.jobId):
                    self.setBackendResultCode(feedback[self.jobId].get('code'))
                    #self.setBackendResultCode(feedback[self.jobId].get('value'))
                    self.setAuto_feedback(feedback[self.jobId].get('value'))
                    #self.setAuto_feedback(feedback[self.jobId].get('message'))
            
                    log("[%s] result value: '%s'" % 
                        (self.getId(), self.getBackendResultCode()))

                    if (parent.getAutoAccept()) and (self.isSolved()):
                        # automatically move this submission into state 
                        # accepted if it passed all tests (solved == True)
                        # and 'autoAccept' is True
                        self._changeWfState('accept', "Automatically checked "
                                            "by '%s' and accepted." % backend)

                        msgId = 'submission_accepted'
                        msgDefault = 'Submission has been accepted.'

                    else:
                        self._changeWfState('retract', "Automatically checked "
                                            "by '%s'." % backend)
        
                else:
                    log('[%s] no feedback after %d polls' % (self.getId(), 
                                                           MAX_WAIT_TIME))
                # end if
            # end if

        except Exception, e:
            log('%s: %s' % (sys.exc_info()[0], e))
            log(''.join(traceback.format_exception(*sys.exc_info())))

            self._changeWfState('retract', 'Auto check failed: %s' % str(e))
            
            result = -42;
            msgId = 'submission_saved_check_failed'
            msgDefault = 'Auto checking this submission failed ' \
                         '(%s).' % (e,)

        message = self.translate(msgid = msgId,
                                 domain = I18N_DOMAIN,
                                 default = msgDefault)
        
        # TODO:
        return (result, message)


    security.declarePublic('getViewModeReadFieldNames')
    def getViewModeReadFieldNames(self):
        """
        Returns the names of the fields which are shown in view mode.
        This method should be overridden in subclasses which need more fields.        

        @see ECAssignment.getViewModeReadFieldNames
        @return list of field names
        """
        fieldNames = ['auto_feedback']
        
        result = ECAssignment.getViewModeReadFieldNames(self)
        
        for name in result:
            if name == 'file':
                i = result.index(name)

                for elem in fieldNames:
                    result.insert(i+1, elem)

                break
        
        return result


    security.declarePublic('getGradeModeReadFieldNames')
    def getGradeModeReadFieldNames(self):
        """
        Returns the names of the fields which are read only in grade mode.
        This method should be overridden in subclasses which need more fields.        

        @return list of field names
        """
        fieldNames = ['auto_feedback']
        
        result = ECAssignment.getGradeModeReadFieldNames(self)
        
        for name in result:
            if name == 'file':
                i = result.index(name)

                for elem in fieldNames:
                    result.insert(i+1, elem)

                break

        return result


    security.declarePublic('getFooIndicators')
    def getIndicators(self):
        """
        Returns a list of dictionaries which contain information necessary
        to display the indicator icons.

        @see ECAssignmentBox.getIndicators
        """
        
        result = []
        
        if hasattr(self, 'backendResultCode'):
            
            resultValue = self.backendResultCode
            resultMessage = re.sub('[\r\n]+', ' ', str(self.auto_feedback))
            
            if type(resultValue) == BooleanType:
    
                if self.isSolved():
                    icon = 'ec_accept.png'
                else:
                    icon = 'ec_error.png'
            
                result.append({'icon':icon, 
                               'alt':'Auto feedback',
                               'alt_msgid':'label_auto_feedback',
                               'title':resultMessage,
                               })
                # end if
            # end if
            elif (type(resultValue) == IntType) and resultValue < 0:
                
                icon = 'ec_exclamation.png'
                
                result.append({'icon':icon, 
                               'alt':'Auto feedback',
                               'alt_msgid':'label_auto_feedback',
                               'title':resultMessage,
                               })
            # end elif
            else:
                result.append({'text':resultValue, 
                               })
            # end else
                
        result.extend(ECAssignment.getIndicators(self))

        return result

registerType(ECAutoAssignment)
