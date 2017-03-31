from uuid import uuid4

import cherrypy

from handlers.session import getUsername


@cherrypy.tools.authorize()
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
@cherrypy.expose
class JourneyHandler(object):

    journeys = {}

    def GET(self, journeyid=None):
        response = {}
        username = getUsername()

        try:
            if not journeyid:
                response = [journey for journey in JourneyHandler.journeys.values() if journey.get('createdBy') == username]
            else:
                journey = JourneyHandler.journeys[journeyid]
                if journey.get('createdBy') == username:
                    response = journey
                else:
                    raise cherrypy.HTTPError(403, 'cannot access journey')
        except KeyError:
            raise cherrypy.HTTPError(404, 'Not Found')

        return response

    def POST(self):
        journey = cherrypy.request.json

        if journey:
            jid = str(uuid4())[24:]
            journey['createdBy'] = getUsername()
            journey['journeyId'] = jid
            JourneyHandler.journeys[jid] = journey
        else:
            raise cherrypy.HTTPError(400, 'data was empty')

        return journey

    def PATCH(self, journeyid):
        journey = cherrypy.request.json

        try:
            orgJourney = JourneyHandler.journeys[journeyid]

            if orgJourney['createdBy'] == getUsername():
                JourneyHandler.journeys[journeyid].update(journey)
                response = JourneyHandler.journeys[journeyid]
            else:
                raise cherrypy.HTTPError(403, 'could not modify {}'.format(journeyid))

        except KeyError:
            raise cherrypy.HTTPError(404, 'no journey with id {} found'.format(journeyid))

        return response

    def DELETE(self, journeyid):
        try:
            journey = JourneyHandler.journeys[journeyid]
            if journey.get('createdBy') == getUsername():
                response = JourneyHandler.journeys.pop(journeyid)
            else:
                raise cherrypy.HTTPError(403, 'cannot access journey')
        except KeyError:
            raise cherrypy.HTTPError(404, 'no journey with id {} found'.format(journeyid))

        return response
