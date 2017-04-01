from handlers.session import SessionHandler
from handlers.journey import JourneyHandler


class Root(object):
    pass


server = Root()

server.session = SessionHandler()
server.journeys = JourneyHandler()
