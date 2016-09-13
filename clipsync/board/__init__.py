import clipboard

from twisted.internet import task


class Clipboard(object):

    def __init__(self, clipboard, clipboard_polling_interval=1.0):
        self._clipboard = clipboard
        self._clipboard_callbacks = []
        self._last_clipboard_value_on_poll = self.value
        self._polling_is_active = False

        task.LoopingCall(self._clipboard_listener).start(clipboard_polling_interval)

    @property
    def value(self):
        try:
            return self._clipboard.paste()
        except:
            return ''

    def copy(self, value):
        self._clipboard.copy(value)
        self._last_clipboard_value_on_poll = value

    def on_clipboard_change(self, callback):
        self._clipboard_callbacks.append(callback)

    def _clipboard_listener(self):
        current_clipboard_value = self.value

        if current_clipboard_value != self._last_clipboard_value_on_poll:
            self._last_clipboard_value_on_poll = current_clipboard_value

            for callback in self._clipboard_callbacks:
                callback(current_clipboard_value)

    @staticmethod
    def create(args=None):
        return Clipboard(clipboard)
