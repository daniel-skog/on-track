import cherrypy

from handlers.session import SessionHandler
from handlers.journey import JourneyHandler
from handlers.game import GameHandler


@cherrypy.expose
class Api(object):

    def GET(self):
        # return info on api...
        pass


server = Api()

server.session = SessionHandler()
server.journeys = JourneyHandler()
server.games = GameHandler()
