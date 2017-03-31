import json as _json

from cherrypy.test import helper


class OnTrackTestHelper(helper.CPWebCase):

    def post(self, url, json=None, body=None, headers=None, **kwargs):
        if json is not None:
            body = _json.dumps(json)
            if not headers:
                headers = []
            headers.append(('Content-Type', 'application/json'))
            headers.append(('Content-Length', str(len(body))))

        self.getPage(url, body=body, method='POST', headers=headers, **kwargs)

        try:
            self.json = _json.loads(self.body)
        except Exception:
            pass

    def get(self, url, **kwargs):
        self.getPage(url, method='GET', **kwargs)

        try:
            self.json = _json.loads(self.body)
        except Exception:
            pass

    def patch(self, url, json=None, body=None, headers={}, **kwargs):
        if json is not None:
            body = _json.dumps(json)
            if not headers:
                headers = []
            headers.append(('Content-Type', 'application/json'))
            headers.append(('Content-Length', str(len(body))))

        self.getPage(url, body=body, method='PATCH', headers=headers, **kwargs)

        try:
            self.json = _json.loads(self.body)
        except Exception:
            pass

    def delete(self, url, **kwargs):
        status, headers, body = self.getPage(url, method='DELETE', **kwargs)

        try:
            body = _json.loads(body)
        except Exception:
            pass

        return status, headers, body

    def put(self, *args, **kwargs):
        self.patch(*args, **kwargs)
