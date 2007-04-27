## Controller Python Script "prefs_backend_set"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Set backends
from Products.CMFCore.utils import getToolByName

REQUEST = context.REQUEST

# resourcestrings
I18N_DOMAIN = 'eduComponents'

# get spooler tool
ecs_tool = getToolByName(context, 'ecspooler_tool')

# save properties
#ecs_tool.manage_changeProperties(REQUEST)
props = context.portal_properties.ecspooler_properties
props.manage_changeProperties(REQUEST)

# save backend IDs
ecs_tool.setSelectedBackends(REQUEST.get('selectedBackends', []))
# cache backends
ecs_tool.manage_cacheBackends()

# set portal message
msg = context.translate(
        msgid   = 'settings_saved',
        domain  = I18N_DOMAIN,
        default = 'Your changes have been saved.')

return state.set(portal_status_message = msg)
#return printed
