import treq
import klein
import json


class Interaction(object):

    def __init__(self, app, encrypt, port=3000, secret='i_am_roy'):
        self._app = app
        self._encrypt = encrypt
        self._port = port
        self._secret = secret
        self._callbacks = []

        self._initialize_app()

    def send_value(self, host, value):
        url = 'http://{0}:{1}/{2}'.format(host, self._port, 'clipboard')
        data = {'value': value}
        headers = {'Content-Type': ['application/json']}

        encrypted_data = self._encrypt.encrypt(json.dumps(data))

        treq.post(url, data=encrypted_data, headers=headers)

    def on_incoming_value(self, callback):
        self._callbacks.append(callback)

    def listen(self):
        self._app.run('0.0.0.0', self._port)

    def _initialize_app(self):
        self._app.route('/clipboard', methods=['POST'])(self._on_incoming_message)

    def _on_incoming_message(self, request):
        decrypted_data = self._encrypt.decrypt(request.content.read())

        try:
            body = json.loads(decrypted_data)
        except:
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
    def create(args):
        app = klein.Klein()

        return Interaction(app, args.encrypt, port=args.port, secret=args.channel)
