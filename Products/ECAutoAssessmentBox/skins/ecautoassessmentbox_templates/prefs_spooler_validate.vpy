## Script (Python) "prefs_spooler_validate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##
REQUEST = context.REQUEST

I18N_DOMAIN = 'eduComponents'

errors = {}

host = REQUEST.get('host', None)
port = REQUEST.get('port', None)
username = REQUEST.get('username', None)
password = REQUEST.get('password', None)

if not host:
	errors['host'] = 'Host required.'

if not port:
	errors['port'] = 'Port required.'

if not username:
	errors['username'] = 'Username required.'

if not password:
	errors['password'] = 'Password required.'


failure_msg = context.translate(
                msgid   = 'ecspooler_settings_invalid',
                domain  = I18N_DOMAIN,
                default = 'Please correct the indicated errors.')

if errors:
    context.plone_utils.addPortalMessage(failure_msg)
    return state.set(status = 'failure', errors = errors)
else:
    return state
