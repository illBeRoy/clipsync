from twisted.internet import reactor

import clipsync.board
import clipsync.interact


a = clipsync.interact.Interaction.create()
b = clipsync.board.Clipboard.create()

a.on_incoming_value(b.copy)
b.on_clipboard_change(lambda x: a.send_value('http://requestb.in', x))

a.listen()
reactor.run()


