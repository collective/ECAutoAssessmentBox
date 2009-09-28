## Script (Python) "validate_recheck"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##
user = context.portal_membership.getAuthenticatedMember()

if not user.has_role(['Owner', 'Reviewer', 'Manager'], context.aq_parent):
    context.plone_utils.addPortalMessage('Your are not allowed to recheck this submission.')
    return state.set(status='failure')
else:
    return state
