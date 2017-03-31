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
        assert len(JourneyHandler.journeys) == 1

    def test_putSetsCreatedBy(self):
        journey = self.journey()

        self.post('/', json=journey)

        self.assertStatus(200)
        assert self.json['createdBy'] == 'testuser'

    def test_putSetsJourneyId(self):
        journey = self.journey()

        self.post('/', json=journey)

        self.assertStatus(200)
        assert self.json['journeyId']

    def test_canGetJourneyById(self):
        journey = self.journey()

        self.post('/', json=journey)
        posted = self.json
        jid = posted['journeyId']
        self.get('/{}'.format(jid))

        self.assertStatus(200)
        assert posted == self.json

    def test_gettingAJourneyCreatedByAnotherUserReturnsForbiddenAccess(self):
        journey = self.journey()

        self.post('/', json=journey)
        jid = self.json.get('journeyId')
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
        journey = self.json
        journey['destination'] = 'ankeborg'
        self.patch('/{}'.format(journey['journeyId']), json=journey)
        self.get('/{}'.format(journey['journeyId']))

        self.assertStatus(200)
        assert self.json.get('destination') == 'ankeborg'

    def test_modificationOfAnotherPlayersJourneyReturnsForbiddenAccess(self):
        journey = self.journey()

        self.post('/', json=journey)
        journey['destination'] = 'ankeborg'
        tools.mockAuthorize.username = 'pineapple'
        self.patch('/{}'.format(self.json['journeyId']), json=journey)

        self.assertStatus(403)

    def test_modifyingANotExistingJourneyReturnsNotFound(self):
        journey = self.journey()

        self.post('/', json=journey)
        journey['destination'] = 'ankeborg'
        self.patch('/asdasdasdasdasd', json=journey)

        self.assertStatus(404)

    def test_canRemoveJourney(self):
        journey = self.journey()

        self.post('/', json=journey)
        self.delete('/{}'.format(self.json['journeyId']))

        self.assertStatus(200)
        assert self.json['journeyId'] not in JourneyHandler.journeys

    def test_removingANotExistingJourneyReturnsNotFound(self):
        journey = self.journey()

        self.post('/', json=journey)
        self.delete('/fsdfdfdssaasd')

        self.assertStatus(404)

    def test_removingAnotherPlayersJourneyReturnsForbiddenAccess(self):
        journey = self.journey()

        self.post('/', json=journey)
        tools.mockAuthorize.username = 'pineapple'
        self.delete('/{}'.format(self.json['journeyId']))

        self.assertStatus(403)
