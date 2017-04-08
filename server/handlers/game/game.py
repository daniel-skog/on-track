

STATE_STARTED = 'started'
STATE_OPEN = 'open'
STATE_FINISHED = 'finished'

OUTCOME_WIN = 'win'
OUTCOME_DRAW = 'draw'

GAME_SOCKET_URI_TEMPLATE = 'api/game/socket'


class Game(object):

    def __init__(self, gameId, title=None, createdBy=None):
        self.gameId = gameId
        self.title = title
        self.createdBy = createdBy

        self.joinedPlayers = []
        self.state = STATE_OPEN
        self.winner = None
        self.outcome = None
        self.gameSocketUri = 'api/game/socket'
        self.journey = None

    def __iter__(self):
        yield 'gameId', self.gameId
        yield 'title', self.title
        yield 'createdBy', self.createdBy
        yield 'joinedPlayers', self.joinedPlayers
        yield 'state', self.state
        yield 'winner', self.winner
        yield 'outcome', self.outcome
        yield 'gameSocketUri', self.gameSocketUri
