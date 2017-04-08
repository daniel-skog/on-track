from uuid import uuid4

import cherrypy

from .game import Game


@cherrypy.tools.authorize()
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
@cherrypy.expose
class GameHandler(object):

    games = {}

    def GET(self, gameid=None):
        if not gameid:
            return [dict(g) for g in GameHandler.games.values()]
        else:
            try:
                return dict(GameHandler.games[gameid])
            except KeyError:
                raise cherrypy.HTTPError(404, 'could not find game with id {}'.format(gameid))

    def POST(self):
        data = cherrypy.request.json

        gameid = str(uuid4())[24:]

        if data:
            title = data.get('title', gameid)
        else:
            title = gameid

        GameHandler.games[gameid] = game = Game(gameid, title=title, createdBy=cherrypy.session.get('username'))

        return dict(game)

    def DELETE(self, gameid):
        try:
            game = GameHandler.games[gameid]
            if game.createdBy != cherrypy.session.get('username'):
                raise cherrypy.HTTPError(403, 'cannot delete game created by another player')
            del GameHandler.games[gameid]
            return dict(game)
        except KeyError:
            raise cherrypy.HTTPError(404, 'could not find game with id {}'.format(gameid))
