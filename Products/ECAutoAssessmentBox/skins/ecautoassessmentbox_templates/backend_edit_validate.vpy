## Script (Python) "validate_base"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##
errors = {}
errors = context.validate(REQUEST=context.REQUEST, errors=errors, data=1, metadata=0)

if errors:
    context.plone_utils.addPortalMessage('Please correct the indicated errors: %s' % errors)
    return state.set(status='failure', errors=errors)
else:
    #context.plone_utils.addPortalMessage('Your changes have been saved.')
    return state
