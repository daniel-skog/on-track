from handlers.session import Session, Login, Logout


class Root(object):
    pass


server = Root()

server.session = Session()
server.session.login = Login()
server.session.logout = Logout()
