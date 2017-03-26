import os.path

import cherrypy

import handlers


STATIC_PATH = os.path.dirname(os.path.realpath(__file__))
STATIC_PATH = os.path.join(STATIC_PATH, '..', 'static')
STATIC_PATH = os.path.normpath(STATIC_PATH)


class Root(object):
    pass


def configure():
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})


def main():
    configure()
    config = {
        '/': {
            'tools.sessions.on': True
        },
        '/api': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    }
    cherrypy.tree.mount(handlers.server, config=config)
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == '__main__':
    main()
