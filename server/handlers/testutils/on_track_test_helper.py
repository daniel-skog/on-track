from unittest.mock import patch

import json as _json

from cherrypy.test import helper
from cherrypy.lib.sessions import RamSession
import cherrypy


def mockWebSocketHandler():
    cherrypy.request.ws_handler = True


cherrypy.tools.mock_ws_handler = cherrypy.Tool('before_handler', mockWebSocketHandler)


class OnTrackTestHelper(helper.CPWebCase):

    def __init__(self, *args, **kwargs):
        super(OnTrackTestHelper, self).__init__(*args, **kwargs)

        self.session = RamSession()

    def login(self, username='testuser'):
        self.session['username'] = username
        self.session['loggedIn'] = True

    def logout(self):
        self.session['username'] = None
        self.session['loggedIn'] = False

    def resetSession(self):
        self.session = RamSession()

    def post(self, url, json=None, body=None, headers=None, **kwargs):
        if not headers:
            headers = []

        if json is not None:
            body = _json.dumps(json)
            headers.append(('Content-Type', 'application/json'))
            headers.append(('Content-Length', str(len(body))))

        with patch('cherrypy.session', self.session, create=True):
            self.getPage(url, body=body, method='POST', headers=headers, **kwargs)

        try:
            self.json = _json.loads(self.body)
        except Exception:
            pass

    def get(self, url, headers=None, **kwargs):
        if not headers:
            headers = []

        with patch('cherrypy.session', self.session, create=True):
            self.getPage(url, method='GET', **kwargs)

        try:
            if self.cookies:
                headers.append(('Cookie', self.cookies))
            self.json = _json.loads(self.body)
            self.setCookies()

        except Exception:
            pass

    def patch(self, url, json=None, body=None, headers=None, **kwargs):
        if not headers:
            headers = []

        if json is not None:
            body = _json.dumps(json)
            headers.append(('Content-Type', 'application/json'))
            headers.append(('Content-Length', str(len(body))))

        with patch('cherrypy.session', self.session, create=True):
            self.getPage(url, body=body, method='PATCH', headers=headers, **kwargs)

        try:
            self.json = _json.loads(self.body)
        except Exception:
            pass

    def delete(self, url, headers=None, **kwargs):
        if not headers:
            headers = []

        with patch('cherrypy.session', self.session, create=True):
            self.getPage(url, method='DELETE', **kwargs)

        try:
            self.json = _json.loads(self.body)
        except Exception:
            pass

    def put(self, *args, **kwargs):
        self.patch(*args, **kwargs)
