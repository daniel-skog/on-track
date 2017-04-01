import cherrypy
import pytest

import tools
from handlers.session import SessionHandler

from handlers.testutils import OnTrackTestHelper


class TestJourney(OnTrackTestHelper):

    def setup_server():

        config = {
            '/': {
                'tools.sessions.on': True,
                'request.dispatch': cherrypy.dispatch.MethodDispatcher()
            }
        }

        cherrypy.tree.mount(SessionHandler(), '/', config=config)

    setup_server = staticmethod(setup_server)

    def test_isNotLoggedInByDefault(self):
        self.get('/')

        self.assertStatus(200)
        assert not self.json['loggedIn']

    def test_canLogIn(self):
        self.post('/', json={'username': 'banana'})

        self.assertStatus(200)
        assert self.json['loggedIn']
        assert self.json['username'] == 'banana'

    def test_loginWithoutUsernameReturnsBadRequest(self):
        self.post('/', json={})

        self.assertStatus(400)

    def test_canLogout(self):
        self.delete('/')

        self.assertStatus(200)
