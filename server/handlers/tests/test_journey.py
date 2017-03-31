import cherrypy
import pytest

import tools
tools.setupMockAuthorize()
from handlers.journey import JourneyHandler

from handlers.testutils import OnTrackTestHelper


class TestJourney(OnTrackTestHelper):

    def journey(self):
        return {
            'destination': 'kvackeby',
            'clues': {
                '10': 'asdasd',
                '8': 'asdasd',
                '6': 'asdasd',
                '4': 'asdasd',
                '2': 'asdasd'
            },
            'questions': {
                '1': {
                    'questionType': '',
                    'answer': '',
                    'question': '?'
                },
                '2': {
                    'questionType': '',
                    'answer': '',
                    'question': '?'
                },
                '3': {
                    'questionType': '',
                    'answer': '',
                    'question': '?'
                }
            }
        }

    def setup_method(self, _):
        JourneyHandler.journeys.clear()
        tools.mockAuthorize.username = 'testuser'

    def setup_server():

        config = {
            '/': {
                'tools.sessions.on': True,
                'request.dispatch': cherrypy.dispatch.MethodDispatcher()
            }
        }

        cherrypy.tree.mount(JourneyHandler(), '/', config=config)

    setup_server = staticmethod(setup_server)

    def test_canPutJourneyInDb(self):
        journey = self.journey()

        self.post('/', json=journey)

        self.assertStatus(200)
        assert len(self.json) == 1

    def test_putSetsCreatedBy(self):
        journey = self.journey()

        self.post('/', json=journey)

        self.assertStatus(200)
        (_, j), = self.json.items()
        assert j['createdBy'] == 'testuser'

    def test_canGetJourneyById(self):
        journey = self.journey()

        self.post('/', json=journey)
        (jid, jput), = self.json.items()
        self.get('/{}'.format(jid))

        self.assertStatus(200)
        assert len(self.json) == 1
        (jid, jget), = self.json.items()
        assert jput == jget

    def test_gettingAJourneyCreatedByAnotherUserReturnsForbiddenAccess(self):
        journey = self.journey()

        self.post('/', json=journey)
        (jid, jput), = self.json.items()
        tools.mockAuthorize.username = 'pineapple'
        self.get('/{}'.format(jid))
        self.assertStatus(403)

    def test_nonexistingJourneyIdReturnsNotFound(self):
        journey = self.journey()

        self.post('/', json=journey)
        self.get('/asdasdasdasdasdasd')
        self.assertStatus(404)

    def test_canGetAllJourneysCreatedByTheUser(self):
        journey = self.journey()

        self.post('/', json=journey)
        self.post('/', json=journey)
        self.post('/', json=journey)
        tools.mockAuthorize.username = 'pineapple'
        self.post('/', json=journey)
        self.post('/', json=journey)
        tools.mockAuthorize.username = 'testuser'
        self.get('/')

        self.assertStatus(200)
        assert len(self.json) == 3

    def test_canModifyJourney(self):
        journey = self.journey()

        self.post('/', json=journey)
        (jid, j), = self.json.items()
        journey['destination'] = 'ankeborg'
        self.patch('/{}'.format(jid), json=journey)
        self.get('/{}'.format(jid))

        self.assertStatus(200)
        (jid, j), = self.json.items()
        assert j.get('destination') == 'ankeborg'

    def test_modifyReturnsTheModifiedJourney(self):
        journey = self.journey()

        self.post('/', json=journey)
        (jid, j), = self.json.items()
        journey['destination'] = 'ankeborg'
        self.patch('/{}'.format(jid), json=journey)

        self.assertStatus(200)
        (jid, j), = self.json.items()
        assert j.get('destination') == 'ankeborg'

    def test_modificationOfAnotherPlayersJourneyReturnsForbiddenAccess(self):
        journey = self.journey()

        self.post('/', json=journey)
        (jid, j), = self.json.items()
        journey['destination'] = 'ankeborg'
        tools.mockAuthorize.username = 'pineapple'
        self.patch('/{}'.format(jid), json=journey)

        self.assertStatus(403)

    def test_modificationWithEmptyJourneyReturnsFormatError(self):
        journey = self.journey()

        self.post('/', json=journey)
        (jid, j), = self.json.items()
        self.patch('/{}'.format(jid), json={})

        self.assertStatus(400)

    def test_modifyingANotExistingJourneyReturnsNotFound(self):
        journey = self.journey()

        self.post('/', json=journey)
        journey['destination'] = 'ankeborg'
        self.patch('/asdasdasdasdasd', json=journey)

        self.assertStatus(404)

    def test_canRemoveJourney(self):
        journey = self.journey()

        self.post('/', json=journey)
        (jid, j), = self.json.items()
        self.delete('/{}'.format(jid))

        self.assertStatus(200)
        assert jid not in JourneyHandler.journeys

    def test_removingANotExistingJourneyReturnsNotFound(self):
        journey = self.journey()

        self.post('/', json=journey)
        self.delete('/fsdfdfdssaasd')

        self.assertStatus(404)

    def test_removingAnotherPlayersJourneyReturnsForbiddenAccess(self):
        journey = self.journey()

        self.post('/', json=journey)
        (jid, j), = self.json.items()
        tools.mockAuthorize.username = 'pineapple'
        self.delete('/{}'.format(jid))

        self.assertStatus(403)
