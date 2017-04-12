import cherrypy


@cherrypy.tools.register('before_handler')
def authorize():
    if not cherrypy.session.get('loggedIn'):
        raise cherrypy.HTTPError(401, 'Not logged in')
