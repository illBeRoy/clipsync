# clipsync
*pythonic cli for zeroconf shared clipboards over local networks*

### what

Copy on computer A, paste on computer B.

### install

Available from pip:

`$ pip install clipsync`

### use

* Start the clipsync daemon:
	1. `$ clipsync start <channel>`
	2. Now every computer on the network which uses clipsync on the same channel will be automatically attached to yours.

* Stop the clipsync daemon:
	1. `$ clipsync stop`
	2. If the daemon was up, it will now be stopped.

### Important notes:
1. Only tested on *nix systems at the moment (mac and linux)
2. Communication is encrypted using AES
