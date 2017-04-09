import os.path
import json

import cherrypy

import tools
import handlers


def standardErrorMessage(status, message, traceback, version):
    response = cherrypy.response
    response.headers['Content-Type'] = 'application/json'
    if status != 500:
        traceback = None
    return json.dumps({'status': status, 'message': message, 'traceback': traceback, 'cpVersion': version, 'appVersion': '0'})


def configure():
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'error_page.default': standardErrorMessage})


def main():
    configure()
    config = {
        '/': {
            'tools.sessions.on': True,
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    }
    cherrypy.tree.mount(handlers.server, '/api', config=config)
    cherrypy.engine.start()
    cherrypy.engine.block()
