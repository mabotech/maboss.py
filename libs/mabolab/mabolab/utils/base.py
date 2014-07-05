"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from kserver.model import meta
from kserver.model.menurole.menurolemodel import *


class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        identity = environ.get('repoze.who.identity')
        if identity:
            c.userid = identity['repoze.who.userid']
            try:
                menurole = MenuRole()
                c.menus = menurole.getUserMenus(c.userid)
            except Exception,e:
                c.error="ERROR : " +e.message
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session_post.remove()
            meta.Session_oracle.remove()
