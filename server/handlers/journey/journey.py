from uuid import uuid4

import cherrypy

from handlers.session import getUsername


@cherrypy.tools.authorize()
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class JourneyHandler(object):

    exposed = True
    journeys = {}

    def GET(self, journeyid=None):
        response = {}
        username = getUsername()

        try:
            if not journeyid:
                response = {jid: journey for jid, journey in JourneyHandler.journeys.items() if journey.get('createdBy') == username}
            else:
                journey = JourneyHandler.journeys[journeyid]
                if journey.get('createdBy') == username:
                    response = {journeyid: journey}
                else:
                    raise cherrypy.HTTPError(403, 'cannot access journey')
        except KeyError:
            raise cherrypy.HTTPError(404, 'Not Found')

        return response

    def POST(self):
        journey = cherrypy.request.json

        if journey:
            jid = str(uuid4())[24:]
            response = {jid: journey}
            journey['createdBy'] = getUsername()
            JourneyHandler.journeys.update(response)
        else:
            raise cherrypy.HTTPError(400, 'data was empty')

        return response

    def PATCH(self, journeyid):
        journey = cherrypy.request.json

        if not journey:
            raise cherrypy.HTTPError(400, 'data was empty')

        try:
            orgJourney = JourneyHandler.journeys[journeyid]

            if orgJourney['createdBy'] == getUsername():
                JourneyHandler.journeys[journeyid].update(journey)
                response = {journeyid: journey}
            else:
                raise cherrypy.HTTPError(403, 'could not modify {}'.format(journeyid))

        except KeyError:
            raise cherrypy.HTTPError(404, 'no journey with id {} found'.format(journeyid))

        return response

    def DELETE(self, journeyid):
        try:
            journey = JourneyHandler.journeys[journeyid]
            if journey.get('createdBy') == getUsername():
                response = {journeyid: JourneyHandler.journeys.pop(journeyid)}
            else:
                raise cherrypy.HTTPError(403, 'cannot access journey')
        except KeyError:
            raise cherrypy.HTTPError(404, 'no journey with id {} found'.format(journeyid))

        return response
