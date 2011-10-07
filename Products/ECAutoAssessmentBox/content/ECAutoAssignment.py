# -*- coding: utf-8 -*-
# $Id$
#
# Copyright (c) 2006-2011 Otto-von-Guericke-UniversitŠt Magdeburg
#
# This file is part of ECAutoAssessmentBox.
#
__author__ = """Mario Amelung <mario.amelung@gmx.de>"""
__docformat__ = 'plaintext'

import sys
import re, time
import traceback

from types import BooleanType
from types import IntType

import interfaces

from AccessControl import ClassSecurityInfo
#from AccessControl import Unauthorized
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager

from zope.interface import implements

from Products.Archetypes.atapi import TextField
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import ComputedWidget
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import registerType 

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.CMFCore.utils import getToolByName

from Products.ECAssignmentBox.content.ECAssignment import ECAssignment

from Products.ECAutoAssessmentBox import config
from Products.ECAutoAssessmentBox import LOG
from Products.ECAutoAssessmentBox.tool import ECSpoolerTool

# set max wait time; after a maxium of 15 tries we will give up getting 
# any result from the spooler until this assignment will be accessed again
MAX_WAIT_TIME = 3
MAX_SLEEP_TIME = 1.2

schema = Schema((

    TextField(
        'auto_feedback',
        #allowable_content_types = ('text/plain',),
        default_output_type = ('text/plain',),
        searchable = True,
        accessor = 'getAutoFeedback',
        widget = ComputedWidget(
            label = "Auto feedback",
            label_msgid = "label_auto_feedback",
            description = "The automatic feedback for this assignment.",
            description_msgid = "help_auto_feedback",
            i18n_domain = config.I18N_DOMAIN,
            macro = 'auto_feedback_widget',
        ),
    ),

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
            i18n_domain = config.I18N_DOMAIN,
        )
    ),

    StringField(
        'jobId',
        searchable = False,
        widget=ComputedWidget(
            modes=('view'),
            label='Job id',
            label_msgid = "label_job_id",
            description = "Job-ID for this assignment.",
            description_msgid = 'help_job_id',
            i18n_domain = config.I18N_DOMAIN,
        ),
    ),

),
)

ECAutoAssignment_schema = ECAssignment.schema.copy() + \
    schema.copy()

class ECAutoAssignment(ECAssignment, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IECAutoAssignment)

    meta_type = 'ECAA'
    _at_rename_after_creation = True

    schema = ECAutoAssignment_schema

    # Methods
    #security.declarePublic('getAutoFeedback')
    def getAutoFeedback(self):
        """
        Returns the message given by the test backend for this submission.  
        If there is no result we will try to get one from spooler/backend.
        
        @return: feedback message as String
        """
        
        if not self.auto_feedback and self.jobId:
            try:
                LOG.debug("Trying to retrieve results from spooler for job: %s" % self.jobId)
        
                ecaab_utils = getToolByName(self, config.ECS_NAME)
                assert ecaab_utils != None, "%s is required." % config.ECS_NAME 
            
                result = ecaab_utils.getResult(self.jobId)
                
                #LOG.debug('xdebug: [%s] result: %s' % (self.getId(), repr(result)))
    
                if result.has_key(self.jobId):
                    self.setBackendResultCode(result[self.jobId].get('value'))
                    self.setAuto_feedback(result[self.jobId].get('message'))
                    
                    auto_accept = self.aq_parent.getAutoAccept()
                    
                    # change workflow state if parent assignment box has auto 
                    # acception enabled.
                    if (auto_accept and self.isSolved()):
                        self._changeWfState('accept', "Automatically tested and accepted.")

                    # 2009-03-30, ma: 
                    # For some reasons we do not put the assignment in 
                    # state pending
                    #else:
                    #    self._changeWfState('retract', "Automatically tested")
                    
            except Exception, e:
                #LOG.error('Error: %s' % str(e))
                LOG.warn('Could not get result from spooler: %s' % str(e))


        instant_feedback = self.aq_parent.getInstantFeedback()
        ecab_utils = getToolByName(self, 'ecab_utils')

        if instant_feedback or ecab_utils.isGrader(self):
            return self.auto_feedback #self.getAuto_feedback()
        else:
            return None


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
        users are not allowed to change workflow states we switch the whole
        security context.
        
        @param transition
        @param comment
        """
        wftool = getToolByName(self, 'portal_workflow')
        # FIXME: we use the 1st workflow for this object, but there can be
        #        more workflows assigned to this object!
        wf = wftool.getWorkflowsFor(self)[0]
        #LOG.debug('xxx: review_state: %s' % wf.getInfoFor(self, 'review_state', ''))
        
        REQUEST = self.REQUEST
        
        # because we switch security context, we have to remember the current user
        currentUser = getSecurityManager().getUser()
        # get user of parent object
        wrappedUser = self.aq_parent.getWrappedOwner() 
        
        #LOG.debug('current user: %s' % currentUser)
        #LOG.debug('wrapped user: %s' % wrappedUser)
        
        # set security context for the owner of the parent object (assignment box)
        newSecurityManager(REQUEST, wrappedUser) 

        #LOG.debug('xxx: %s' % repr(wftool.getTransitionsFor(self, REQUEST=REQUEST)))
        #LOG.debug('xxx: isActionSupported(%s): %s' % (transition, wf.isActionSupported(self, transition)))
        
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
                LOG.warn('Unsupported workflow action %s for object %s.' % (repr(transition), repr(self)))
            
            #except Exception, e:
            #    LOG.error(e)
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
        msgMapping = {}
        
        # get the selected backend in the parent box
        backend = parent.getBackend()
        
        
        if backend == ECSpoolerTool.BACKEND_NONE:
            # behave like a normal assginment box
            return ECAssignment.evaluate(self, parent)
        
        try:
            # get input fields needed by this backend
            inputFields = parent.getInputFields()
            # get selected tests provided by this backend
            tests = parent.getTests()

            # set student solution 
            studentSolution = self.getAsPlainText()
            
            #LOG.debug('xxx: %s' % studentSolution)
            #LOG.debug('xxx: %s' % studentSolution.decode('unicode_escape'))
            
            if not studentSolution:
                # FIXME: translate error message
                raise Exception('Submission is not plain text.')
  
            # HINT, 2009-03-30, ma: 
            # For some reasons we do not put the assignment in state pending
            #self._changeWfState('review', "Queued for automatic testing")
    
            spoolerWSI =  getToolByName(self, config.ECS_NAME)
            assert spoolerWSI != None, "A valid portal ecspooler is required."
    
            # enqueue students' solution
            # TODO: rename sample_soution to model_solution
    
            job = spoolerWSI.appendJob(backend, studentSolution, 
                                       inputFields, tests)

            LOG.debug('[%s] enqueue: %s' % (self.getId(), repr(job)))
            
            # An error occured; return error message
            if job[0] < 0:
                result = job[0];
                msgId = 'submission_saved_check_failed'
                msgDefault = 'Testing this submission failed (exc).'
                msgMapping = {'exc': job[1]}
            else:
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
                    #self.setBackendResultCode(feedback[self.jobId].get('code'))
                    self.setBackendResultCode(feedback[self.jobId].get('value'))
                    #self.setAuto_feedback(feedback[self.jobId].get('value'))
                    self.setAuto_feedback(feedback[self.jobId].get('message'))
            
                    LOG.debug("[%s] result value: '%s'" % 
                        (self.getId(), self.getBackendResultCode()))

                    if (parent.getAutoAccept()) and (self.isSolved()):
                        # automatically move this submission into state 
                        # accepted if it passed all tests (solved == True)
                        # and 'autoAccept' is True
                        self._changeWfState('accept', "Automatically tested and accepted.")

                        msgId = 'submission_accepted'
                        msgDefault = 'Submission has been accepted.'

                    # HINT, 2009-03-30, ma: 
                    # For some reasons we do not put the assignment in 
                    # state pending
                    #else:
                    #    self._changeWfState('retract', "Automatically tested")
        
                else:
                    LOG.warn('[%s] no feedback after %d polls' % (self.getId(), 
                                                           MAX_WAIT_TIME))

                    msgId = 'submission_saved_no_feedback'
                    msgDefault = 'No feedback available.'
                # end if
            # end if

        except Exception, e:
            LOG.debug('%s: %s' % (sys.exc_info()[0], e))
            LOG.debug(''.join(traceback.format_exception(sys.exc_info())))

            #self._changeWfState('retract', 'Auto check failed: %s' % str(e))
            
            result = -42;
            msgId = 'submission_saved_check_failed'
            msgDefault = 'Testing this submission failed (${exc}).'
            msgMapping = {'exc': str(e)}

        message = self.translate(msgid = msgId,
                                 domain = config.I18N_DOMAIN,
                                 default = msgDefault,
                                 mapping = msgMapping)
        
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


    security.declarePublic('getIndicators')
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
                    icon = 'ec_exclamation.png'
            
                result.append({'icon':icon, 
                               'alt':'Auto feedback',
                               'alt_msgid':'label_auto_feedback',
                               'title':resultMessage,
                               })
                # end if
            # end if
            elif (type(resultValue) == IntType) and resultValue < 0:
                
                icon = 'ec_error.png'
                
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

registerType(ECAutoAssignment, config.PROJECTNAME)
# end of class ECAutoAssignment
