import treq
import klein
import json


class Interaction(object):

    def __init__(self, app, port=3000, secret='i_am_roy'):
        self._app = app
        self._port = port
        self._secret = secret
        self._callbacks = []

        self._initialize_app()

    def send_value(self, host, value):
        url = 'http://{0}:{1}/{2}'.format(host, self._port, 'clipboard')
        data = {'secret': self._secret, 'value': value}
        headers = {'Content-Type': ['application/json']}

        treq.post(url, data=json.dumps(data), headers=headers)

    def on_incoming_value(self, callback):
        self._callbacks.append(callback)

    def listen(self):
        self._app.run('0.0.0.0', self._port)

    def _initialize_app(self):
        self._app.route('/clipboard', methods=['POST'])(self._on_incoming_message)

    def _on_incoming_message(self, request):
        body = json.loads(request.content.read())

        if not isinstance(body, dict) or body.get('secret') != self._secret:
            request.setResponseCode(401)
            return ''

        try:
            value = body['value']
        except:
            request.setResponseCode(400)
            return ''

        for callback in self._callbacks:
            callback(value)

        request.setResponseCode(200)
        return ''

    @staticmethod
    def create(args=None):
        app = klein.Klein()

        return Interaction(app)
