import os
import signal
import detach

import clipsync.board
import clipsync.interact
import clipsync.discovery


class Application(object):

    _daemon_pid_path = '/tmp/clipsync_pid'

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
    def _stop_previous_daemon():
        try:
            with open(Application._daemon_pid_path, 'r') as f:
                pid = int(f.read())

            os.kill(pid, signal.SIGKILL)
            os.remove(Application._daemon_pid_path)
            return True
        except:
            return False

    @staticmethod
    def _save_daemon_pid(pid):
        with open(Application._daemon_pid_path, 'w') as f:
            f.write(str(pid))

    @staticmethod
    def run_with_args(args):
        with detach.Detach() as d:
            if d.pid:
                Application._stop_previous_daemon()
                Application._save_daemon_pid(d.pid)
                print 'clipsync started on channel {0}'.format(args.channel)
            else:
                clipboard = clipsync.board.Clipboard.create(args)
                interaction = clipsync.interact.Interaction.create(args)
                discovery = clipsync.discovery.Discovery.create(args)

                app = Application(clipboard, interaction, discovery)
                app._start()

    @staticmethod
    def stop_with_args(args):
        if Application._stop_previous_daemon():
            print 'clipsync was stopped'
        else:
            print 'clipsync could not be stopped or was not running'
