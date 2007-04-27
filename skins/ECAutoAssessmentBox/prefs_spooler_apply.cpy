## Controller Python Script "prefs_spooler_apply"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Reconfigure the ECSpooler
from Products.CMFCore.utils import getToolByName

REQUEST = context.REQUEST

# resourcestrings
I18N_DOMAIN = 'eduComponents'

# get spooler tool
ecs_tool = getToolByName(context, 'ecspooler_tool')

#ecs_tool.manage_changeProperties(REQUEST)
props = context.portal_properties.ecspooler_properties
props.manage_changeProperties(REQUEST)

# test connection without saving
result = ecs_tool.test()

if result:
    msg = context.translate(msgid = 'test_succeeded', domain = I18N_DOMAIN,
                            default = 'Your changes have been saved. '
                                      'Following backends are available: %s. '
                                      %  result
                            )
else:
    msg = context.translate(msgid = 'test_failed', domain = I18N_DOMAIN,
                            default = 'Service not responding (%s:%s).' %
                                      (REQUEST.get('host', ''), 
                                       REQUEST.get('port', ''))
                            )

return state.set(portal_status_message = msg)