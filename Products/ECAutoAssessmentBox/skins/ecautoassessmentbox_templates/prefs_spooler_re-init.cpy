## Controller Python Script "prefs_backend_clear"
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

# reset backend IDs
#ecs_tool.setSelectedBackends([])

# clear backend cache and re-init it
ecs_tool.manage_cacheBackends(reinit=True)

# set portal message
msg = context.translate(
        msgid   = 'cache_reseted',
        domain  = I18N_DOMAIN,
        default = 'Backend cache has been reinitialized.')

context.plone_utils.addPortalMessage(msg)
return state
