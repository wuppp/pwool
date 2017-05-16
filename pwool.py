# -*- coding:utf-8 -*-

'''
@file: pwool.py
@author: Roc木木
@time: 17-4-24 下午11:38
'''

import argparse
from sys import argv
from modules.webdirscan.asyncScan import dirscan
from modules.sshscan.sshscan import sshscan

# def usage(argv):
# 	description = "pwool tools"
# 	parser = argparse.ArgumentParser(description=description)
#
# 	parser.add_argument("-u", "--url", dest="scanUrl", help="the website to be scan", type=str)
# 	parser.add_argument("-d", "--dict", dest="scanDict", help="the dictionary for scan", type=str, default="dict/dict.txt")
# 	parser.add_argument("-c", "--concurrent", dest="concurrentNum", help="concurrent number", type=int, default=20)
# 	# add ssh scan
# 	parser.add_argument("-s", "--ssh", action='store_true', help="ssh scan", dest="sshScan")
#
# 	args = parser.parse_args()
# 	print(args)
# 	return args

def usage():
	usages = """usage: pwool.py type [-h]"""
	return usages

if __name__ == '__main__':
	if len(argv) <= 1:
		print(usage())

	func = argv[1]
	if func in ['dirscan', 'sshscan']:
		eval(func + '(' + str(argv[2:]) + ')')
	else:
		if '-h' in argv or '--help' in argv:
			print(usage())
			exit()
		print(func + " don't kown.\nyou should input ['dirscan', 'sshscan']")
