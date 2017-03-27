
import cherrypy
from handlers.session import getSession


class Login(object):

    exposed = True

    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json

        try:
            cherrypy.session['username'] = data['username']
            cherrypy.session['logged_in'] = True

            return getSession()

        except KeyError as e:
            raise cherrypy.HTTPError(400, 'keyerror: {}'.format(e))
