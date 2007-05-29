# external method
import time
import types

from Products.CMFCore.utils import getToolByName

#from Products.ECAutoAssignmentBox.ECAutoAssignmentBox import ECAutoAssignmentBox
#from Products.ECAutoAssignmentBox.ECAutoAssignment import ECAutoAssignment
from Products.ECAutoAssessmentBox.ECAutoAssessmentBox import ECAutoAssessmentBox
from Products.ECAutoAssessmentBox.ECAutoAssignment import ECAutoAssignment


def change_ecaab_portal_type(self):
    output = u'Time-stamp: <%s>\n' % time.strftime("%Y%m%d %H:%M:%S")
    
    catalog = getToolByName(self, 'portal_catalog')
    
    brains = catalog.searchResults(portal_type = 'ECAutoAssignmentBox',)

    for brain in brains:
        ecaab = brain.getObject()

        output += u'---------------------------------------\n'
        output += u'Title:            %s\n' % ecaab.title
        output += u'Id:               %s\n' % ecaab.getId()
        #output += u'Creator:          %s\n' % ecaab.Creator()
        #output += u'Description:      %s\n' % ecaab.Description().decode('utf8')
        output += u'Portal Type:      %s\n' % ecaab.portal_type
        #output += u'Meta Type:        %s\n' % ecaab.meta_type
        output += u'Class:            %s\n' % ecaab.__class__

        ecaab.portal_type = "ECAAB"
        ecaab.meta_type = "ECAAB"
        ecaab.__class__ = ECAutoAssessmentBox

    return output


def change_ecaa_portal_type(self):
    output = u'Time-stamp: <%s>\n' % time.strftime("%Y%m%d %H:%M:%S")
    
    catalog = getToolByName(self, 'portal_catalog')
    
    brains = catalog.searchResults(portal_type = 'ECAutoAssignment')

    for brain in brains:
        ecaa = brain.getObject()

        output += u'---------------------------------------\n'
        output += u'Title:            %s\n' % ecaa.title
        output += u'Id:               %s\n' % ecaa.getId()
        #output += u'Creator:          %s\n' % ecaa.Creator()
        output += u'Portal Type:      %s\n' % ecaa.portal_type
        #output += u'Meta Type:        %s\n' % ecaa.meta_type
        output += u'Class:            %s\n' % ecaa.__class__
        output += u'ResultCode        %s (%s)\n' % (ecaa.getBackendResultCode(), type(ecaa.getBackendResultCode()))
        
        ecaa.portal_type = "ECAA"
        ecaa.meta_type = "ECAA"
        ecaa.__class__ = ECAutoAssignment

    return output


def change_ecaa_result_type(self):
    output = u'Time-stamp: <%s>\n' % time.strftime("%Y%m%d %H:%M:%S")
    
    catalog = getToolByName(self, 'portal_catalog')
    
    brains = catalog.searchResults(portal_type = 'ECAA')

    for brain in brains:
        ecaa = brain.getObject()

        output += u'---------------------------------------\n'
        output += u'Title:            %s\n' % ecaa.title
        output += u'Id:               %s\n' % ecaa.getId()
        #output += u'Creator:          %s\n' % ecaa.Creator()
        output += u'Portal Type:      %s\n' % ecaa.portal_type
        #output += u'Meta Type:        %s\n' % ecaa.meta_type
        output += u'Class:            %s\n' % ecaa.__class__
        output += u'ResultCode        %s (%s)\n' % (ecaa.getBackendResultCode(), type(ecaa.getBackendResultCode()))
        
        bRC = ecaa.getBackendResultCode()

        if type(bRC) == types.IntType:
            if bRC == 0:
                ecaa.setBackendResultCode(False)
            elif bRC > 0:
                ecaa.setBackendResultCode(True)

    return output


def recheck_ecaa_(self):
    output = u'Time-stamp: <%s>\n' % time.strftime("%Y%m%d %H:%M:%S")
    
    catalog = getToolByName(self, 'portal_catalog')
    
    brains = catalog.searchResults(path={'query':'/'.join(here.getPhysicalPath()), 'depth':1, },
                                   portal_type = 'ECAA'
                                   )
    for brain in brains:

        output += u'---------------------------------------\n'
        output += u'Id:               %s\n' % brain.id
        output += u'State:            %s\n' % brain.review_state

        if brain.review_state == 'submitted':
            output += u'---------------------------------------\n'
            output += u'Id:               %s\n' % brain.id
            
            ecaa = brain.getObject()
            ecaa.ecaa_recheck

    return output
