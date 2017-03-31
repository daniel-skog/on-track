import cherrypy


@cherrypy.tools.register('before_finalize')
def authorize():
    if not cherrypy.session.get('loggedIn'):
        raise cherrypy.HTTPError(401, 'Not Logged In')


def mockAuthorize():
    if mockAuthorize.failAuth:
        raise cherrypy.HTTPError(401, 'Not Logged In')
    else:
        cherrypy.session['username'] = mockAuthorize.username
        cherrypy.session['loggedin'] = True


mockAuthorize.failAuth = False
mockAuthorize.username = 'testuser'


def setupMockAuthorize():
    cherrypy.tools.authorize = cherrypy.Tool('before_handler', mockAuthorize)
