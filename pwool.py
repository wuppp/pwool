# -*- coding:utf-8 -*-

"""
@file: pwool.py
@author: Roc木木
@time: 17-4-24 下午11:38
"""


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
        usage() if '-h' in sys.argv or '--help' in sys.argv else print(func + " don't kown.\n"
                                                                              "you should input ['dir', 'ssh']")
