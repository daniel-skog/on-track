import cherrypy

from handlers.session import SessionHandler
from handlers.journey import JourneyHandler


@cherrypy.expose
class Api(object):

    def GET(self):
        # return info on api...
        pass


server = Api()

server.session = SessionHandler()
server.journeys = JourneyHandler()
