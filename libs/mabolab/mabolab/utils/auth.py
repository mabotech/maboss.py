from pylons import request,response
from pylons.controllers.util import abort, redirect_to
from routes.util import url_for

from repoze.what.plugins.quickstart import setup_sql_auth
from repoze.what.plugins.pylonshq import ActionProtector, \
                                         ControllerProtector

from kserver.model.auth import User, Group, Permission
from kserver.model import meta
from kserver.lib.helpers import flash

def cool_denial_handler(reason):
    # When this handler is called, response.status has two possible values:
    # 401 or 403.
    if response.status.startswith('401'):
        message = 'Oops, you have to login: %s' % reason
    else:
        identity = request.environ['repoze.who.identity']
        userid = identity['repoze.who.userid']
        message = "Come on, %s, you know you can't do that: %s" % (userid,
                                                                   reason)
    flash(message)
    #abort(response.status_int, comment=reason)
    redirect_to(url_for('/'))


def add_auth(app, skip_authentication):
    """
    Add auth middleware to the ``app`` application.
    
    :param app: The WSGI application.
    :param skip_authentication: Should authentication be skipped while testing
        protected areas? (officially recommended)
    
    """
    
    securedapp = setup_sql_auth(app, User, Group, Permission, meta.Session_post,
                                logout_handler='/logout',
                                post_login_url='/post_login',
                                post_logout_url='/post_logout',
                                log_level="info", 
                                skip_authentication=skip_authentication)
    
    return securedapp


class protect_action(ActionProtector):
    # Our denial handler should flash the denial reason:
    default_denial_handler = staticmethod(flash)


class protect_controller(ControllerProtector):
    protector = protect_action


# CoolActionProtector, CoolControllerProtector
class CoolActionProtector(ActionProtector):
    default_denial_handler = staticmethod(cool_denial_handler)

class CoolControllerProtector(ControllerProtector):
    default_denial_handler = staticmethod(cool_denial_handler)

