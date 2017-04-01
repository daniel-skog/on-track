import cherrypy


def getSession():
    return {
        'username': cherrypy.session.get('username'),
        'loggedIn': cherrypy.session.get('loggedIn', False)
    }


def getUsername():
    return cherrypy.session.get('username')


@cherrypy.tools.json_out()
@cherrypy.tools.json_in()
@cherrypy.expose
class SessionHandler(object):

    def GET(self):
        return getSession()

    def POST(self):
        data = cherrypy.request.json

        try:
            cherrypy.session['username'] = data['username']
            cherrypy.session['loggedIn'] = True

            return getSession()

        except KeyError as e:
            raise cherrypy.HTTPError(400, 'keyerror: {}'.format(e))

    def DELETE(self):
        cherrypy.session['username'] = None
        cherrypy.session['loggedIn'] = False

        return getSession()
