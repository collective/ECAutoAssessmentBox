<!-- -*- coding: utf-8 -*- -->

Overview

  ECAutoAssessmentBox is a Plone product derived from ECAssignmentBox 
  and provides special support for automatic evaluation of student 
  submissions, e.g., programming assignments.
  
  Basically ECAutoAssessmentBox works like ECAssignmentBox.  Automatic 
  assessment of programs is handled by ECSpooler (available separately) 
  which manages a submission queue and several backends.  When a student 
  submits a program, it is routed to the backend specified by the 
  teacher for this assignment.  The results of the tests performed by 
  the backend are immediately returned and displayed.

Download

  * "Project page":http://wdok.cs.uni-magdeburg.de/software/

  * "plone.org products page":http://plone.org/products/ecautoassessmentbox/

Prerequisites

 1. To use ECAutoAssessmentBox you need a Plone 2.1.x or 2.5.x
    installation.  Check "plone.org":http://plone.org/products/plone
    for Plone's prerequisites.

 2. The "ECAssignmentBox":http://plone.org/products/ecassignmentbox/ product.

Installation

 If you have a suitable Zope/Plone installation, you can install
 ECAutoAssessmentBox as follows:

 1. Extract the ECAssignmentBox archive into the 'Products' directory
    of your Zope instance. (You can find out where your Zope instance
    is installed by opening the Zope Management Interface (ZMI) and
    going to the Control Panel; the directory listed as
    'INSTANCE_HOME' is what you're looking for.)

 2. Extract the ECAutoAssessmentBox archive into the 'Products'
    directory of your Zope instance.

 3. Restart Zope.

 4. Log in to your Plone site as a manager and use the "Add/Remove
    Products" tool under "Site Setup" to install ECAssignmentBox and
    ECAutoAssessmentBox in this Plone site.  Alternatively, in the
    ZMI, you can use the 'portal_quickinstaller' of the Plone site in
    which you want to use ECAutoAssessmentBox.  In both cases, check
    the boxes next to ECAssignmentBox and ECAutoAssessmentBox and
    click "Install".

Support

  For questions and discussions about ECAutoAssessmentBox, please join the
  "eduComponents mailing
  list":https://listserv.uni-magdeburg.de/mailman/listinfo/educomponents.

Credits

  ECAutoAssessmentBox was written by "Mario
  Amelung":mailto:mario.amelung@gmx.de and
  "Michael Piotrowski":mailto:mxp@dynalabs.de.

  The icons used in ECAutoAssessmentBox are from the "Silk icon
  set":http://www.famfamfam.com/lab/icons/silk/ by Mark James.  They
  are licensed under a "Creative Commons Attribution 2.5
  License":http://creativecommons.org/licenses/by/2.5/.

License

 ECAutoAssessmentBox is licensed under the
 "GPL":http://opensource.org/licenses/gpl-license.

 Copyright © 2006 Otto-von-Guericke-Universität Magdeburg

 ECAutoAssessmentBox is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 ECAutoAssessmentBox is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with ECAutoAssessmentBox; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

