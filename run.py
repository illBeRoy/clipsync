#!/usr/bin/env python
import argparse

import clipsync


def main():
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest='command')

    cmd_start = commands.add_parser('start', help='start clipsync daemon')
    cmd_start.add_argument('channel', help='will only acknowledge peers on same channel')
    cmd_start.add_argument('-p', '--port', type=int, default=21013, help='tcp communication port')

    cmd_stop = commands.add_parser('stop', help='stop clipsync daemon')

    args = parser.parse_args()

    if args.command == 'start':
        clipsync.Application.run_with_args(args)
    elif args.command == 'stop':
        clipsync.Application.stop_with_args(args)


if __name__ == '__main__':
    main()
