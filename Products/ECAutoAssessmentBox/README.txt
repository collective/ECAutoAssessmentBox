Overview
========

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
========

`plone.org products page`_

.. _plone.org products page: http://plone.org/products/ecautoassessmentbox/


Prerequisites
=============

#. To use ECAutoAssessmentBox you need a current Plone installation, 
   specifically Plone 3.  Check `plone.org`_ for Plone's
   prerequisites.

#. The `ECAssignmentBox`_ product.

.. _plone.org :http://plone.org/products/plone
.. _ECAssignmentBox: http://plone.org/products/ecassignmentbox/


Installation
============

See the `Installing an Add-on Product`_ tutorial for more detailed 
product installation instructions.
        
.. _Installing an Add-on Product: http://plone.org/documentation/tutorial/third-party-products/installing


Installing with buildout
------------------------

If you are using `buildout`_ to manage your instance installing 
ECAutoAssessmentBox is very simple.  You can install it by adding it 
to the eggs line for your instance::

  [instance]
  eggs =
      ... 
      Products.ECAutoAssessmentBox

After updating the configuration you need to run ``bin/buildout``, 
which will take care of updating your system.

Then restart your zope instance and use the Add/Remove products page
in Site Setup to install ECAutoAssessmentBox.

.. _buildout: http://pypi.python.org/pypi/zc.buildout


Installing without buildout
---------------------------

Move (or symlink) the ``ECAutoAssessmentBox`` folder of this project
(``Products.ECAutoAssessmentBox/Products/ECAutoAssessmentBox``) into 
the ``Products`` directory of the Zope instance it has to be installed 
for, and restart the server.  Use the Add/Remove products page in 
Site Setup to install ECAutoAssessmentBox.


Support
=======

For questions and discussions about ECAutoAssessmentBox, please join the
`eduComponents mailing list`_.

.. _eduComponents mailing list: https://listserv.uni-magdeburg.de/mailman/listinfo/educomponents.


Credits
=======

ECAssignmentBox was written by `Mario Amelung`_ and 
`Michael Piotrowski`_.

The icons used in ECAssignmentBox are from the `Silk icon set`_ by 
Mark James.  They are licensed under a `Creative Commons Attribution 
2.5 License`_.

ECAutoAssessmentBox was ported to Plone 3 by `Eudemonia Solutions AG`_ 
with support from `Katrin Krieger`_ and the Otto-von-Guericke 
University of Magdeburg.

.. _Mario Amelung: mario.amelung@gmx.de
.. _Michael Piotrowski: mxp@dynalabs.de
.. _Silk icon set: http://www.famfamfam.com/lab/icons/silk/
.. _Creative Commons Attribution 2.5 License: http://creativecommons.org/licenses/by/2.5/
.. _Eudemonia Solutions AG: http://www.eudemonia-solutions.de/
.. _Katrin Krieger: http://wdok.cs.uni-magdeburg.de/Members/kkrieger/
