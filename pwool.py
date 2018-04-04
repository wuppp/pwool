#!/usr/local/bin/env python3

from modules.webdirscan.asyncScan import dir_scan
from modules.sshscan.sshscan import sshscan
import sys


def usage():
    usages = """usage: {filename} type [-h]""".format(filename=sys.argv[0])
    print(usages)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        usage()
        exit()

    func = sys.argv[1]

    if func == "dir":
        dir_scan(sys.argv[2:])
    elif func == "ssh":
        sshscan(sys.argv[2:])
    else:
        if '-h' in sys.argv or '--help' in sys.argv:
            usage()
        else:
            print(func + " don't kown.\nyou should input ['dir', 'ssh']")
