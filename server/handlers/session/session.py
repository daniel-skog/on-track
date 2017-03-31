
import cherrypy


def getSession():
    return {
        'username': cherrypy.session.get('username'),
        'logged_in': cherrypy.session.get('logged_in', False)
    }


def getUsername():
    return cherrypy.session.get('username')


class Session(object):

    exposed = True

    @cherrypy.tools.json_out()
    def GET(self):
        return {
            'username': cherrypy.session.get('username'),
            'logged_in': cherrypy.session.get('logged_in', False)
        }
