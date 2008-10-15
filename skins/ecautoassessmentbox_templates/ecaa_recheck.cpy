## Script (Python) "ecaa_recheck"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

I18N_DOMAIN = 'eduComponents'

REQUEST  = container.REQUEST
RESPONSE = REQUEST.RESPONSE

# get the parent
parent = context.aq_parent

# check this submission again (parameter 'recheck' must be True
result = context.evaluate(parent, True)
            
if result[0]:
    msg = context.translate(
        msgid   = 'submission_rechecked',
        domain  = I18N_DOMAIN,
        default = 'Submission has been rechecked.')

    msg += ' ' + result[1]

    context.plone_utils.addPortalMessage(msg)
    return state

else:
    context.plone_utils.addPortalMessage(result)
    return state.set(status='failure')
