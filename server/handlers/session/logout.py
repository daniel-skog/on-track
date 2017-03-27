
import cherrypy
from handlers.session import getSession


class Logout(object):

    exposed = True

    def POST(self):
        cherrypy.session['username'] = None
        cherrypy.session['logged_in'] = False

        return getSession()
