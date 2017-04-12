import cherrypy
import pytest

from handlers.game import GameHandler
from handlers.testutils import OnTrackTestHelper


class TestJourney(OnTrackTestHelper):

    def setup_method(self, _):
        GameHandler.games.clear()
        self.login()

    def setup_server():

        config = {
            '/': {
                'tools.sessions.on': True,
                'request.dispatch': cherrypy.dispatch.MethodDispatcher()
            }
        }

        cherrypy.tree.mount(GameHandler(), '/', config=config)

    setup_server = staticmethod(setup_server)

    def test_canCreateGame(self):
        assert len(GameHandler.games) == 0
        self.post('/', json={})

        self.assertStatus(200)
        assert len(GameHandler.games) == 1

    def test_createGameReturnsGame(self):
        self.post('/', json={})

        self.assertStatus(200)
        assert 'gameId' in self.json
        assert 'title' in self.json
        assert 'createdBy' in self.json
        assert 'joinedPlayers' in self.json
        assert 'state' in self.json
        assert 'winner' in self.json
        assert 'outcome' in self.json
        assert 'gameSocketUri' in self.json

    def test_createGameSetsCreatedByToTheUserCreatingTheGame(self):
        self.post('/', json={})

        self.assertStatus(200)
        assert self.json.get('createdBy') == 'testuser'

    def test_canReadGameFromId(self):
        self.post('/', json={})
        gameid = self.json['gameId']

        self.get('/{}'.format(gameid))
        self.assertStatus(200)
        assert self.json.get('gameId') == gameid

    def test_canDeleteGame(self):
        self.post('/', json={})
        gameid = self.json['gameId']

        self.delete('/{}'.format(gameid))
        self.assertStatus(200)
        assert gameid not in [g.gameId for g in GameHandler.games.values()]

    def test_cannotDeleteGameCreatedByAnotherPlayer(self):
        self.post('/', json={})
        gameid = self.json['gameId']

        self.login(username='anotheruser')

        self.delete('/{}'.format(gameid))
        self.assertStatus(403)
