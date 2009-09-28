from datetime import datetime

from Acquisition import aq_inner
from kss.core import KSSView, kssaction

class DemoView(KSSView):

    @kssaction
    def response1(self, backend):
        """
        """
        context = aq_inner(self.context)
        
        date = str(datetime.now()) 
        
        # KSS specific calls
        coreCommands = self.getCommandSet('core')
        zopeCommands = self.getCommandSet('zope')
        ploneCommands = self.getCommandSet('plone')

        oldbackend = context.backend

        if (oldbackend <> backend):
            context.setBackend(backend)
           
        #selector = ksscore.getHtmlIdSelector('fieldset-backend')
        #ksszope.refreshViewlet(selector,
        #                       manager='plone.belowcontentbody',
        #                       name='ecaab.content.backend')
        
        #ksszope.refreshProvider('#fieldset-backend', 'plone.belowcontentbody')
        #selector = coreCommands.getCssSelector('.contentViews')
        selector = ksscore.getHtmlIdSelector('ecaab-base-edit')
        
        zopeCommands.refreshViewlet(selector, 
                                    'plone.contentviews',
                                    'plone.contentviews')

        ploneCommands.issuePortalMessage('Yes we can! %s ; %s ; %s ; %s' % 
                                 (date, oldbackend, context.backend, selector), msgtype='info')
