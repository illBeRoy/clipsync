from twisted.internet import reactor

import clipsync.board
import clipsync.interact
import clipsync.discovery


class Application(object):

    def __init__(self, clipboard, interaction, discovery):
        self._clipboard = clipboard
        self._interaction = interaction
        self._discovery = discovery

    def _start(self):
        self._clipboard.on_clipboard_change(self._clipboard_value_has_changed)
        self._interaction.on_incoming_value(self._value_received_from_peer)

        self._discovery.start()
        self._interaction.listen()

    def _clipboard_value_has_changed(self, value):
        for peer in self._discovery.peers:
            self._interaction.send_value(peer, value)

    def _value_received_from_peer(self, value):
        self._clipboard.copy(value)

    @staticmethod
    def run_with_args(args=None):
        clipboard = clipsync.board.Clipboard.create()
        interaction = clipsync.interact.Interaction.create()
        discovery = clipsync.discovery.Discovery.create()

        app = Application(clipboard, interaction, discovery)
        app._start()
        reactor.run()
