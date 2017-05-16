# -*- coding:utf-8 -*-

'''
@file: sshscan.py
@author: Roc木木
@time: 17-4-28 下午2:40
'''

import paramiko, argparse, threading, queue

class SSHConnect:
	def __init__(self, ip, dictPath, port=22, timeout=5, threadNum=20):
		self.passwd = ''
		self.username = ''
		self.dictPath = dictPath
		self.ip = ip
		self.port = port
		self.timeout = timeout
		self.threadNum = threadNum

		self.queue = queue.Queue()
		self._loadDict()

		self.lock = threading.Lock()
		self.isFind = False

	def _loadDict(self):
		with open(self.dictPath) as dict:
			for each in dict:
				if each[0] != '#':
					self.queue.put_nowait(each.strip().split(' '))

	def _connection(self):
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		while not self.queue.empty() and self.isFind is False:	# not empty
			username, passwd = self.queue.get_nowait()
			self.lock.acquire()
			print('[*] Testting: ' + username + ' ' + passwd)
			self.lock.release()
			try:
				ssh.connect(self.ip, self.port, username, passwd, timeout=self.timeout)
				ssh.close()
				self.lock.acquire()
				print('[+] Found the username and password: ' + username + ' ' + passwd)
				self.lock.release()
				self.isFind = True
			except paramiko.ssh_exception.AuthenticationException:
				pass
		ssh.close()

	def run(self):
		threads = []
		for _ in range(self.threadNum):
			thread = threading.Thread(target=self._connection)
			thread.start()
			threads.append(thread)

		for t in threads:
			t.join()

		if self.isFind is False:
			print('[-] No Found')


def __usage(arg):
	description = "sshscan is a simple ssh password scan tools"
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument("scanHost", help="the host to be scan", type=str)
	# parser.add_argument("website", help="the website to be scan", type=str)
	parser.add_argument("-d", "--dict", dest="scanDict", help="the dictionary for scan", type=str, default="dict.txt")
	parser.add_argument("-c", "--thread", dest="threadNum", help="the number of thread", type=int, default=20)
	parser.add_argument("-t", "--timeout", dest="timeout", help="the number of timeout", type=float, default=0.1)
	parser.add_argument("-p", "--port", dest="scanPort", help="the port of ssh", type=int, default=22)
	args = parser.parse_args(arg)
	return args


def sshscan(args):
	arg = __usage(args)
	ssh = SSHConnect(arg.scanHost, arg.scanDict, threadNum=arg.threadNum, timeout=arg.timeout, port=arg.scanPort)
	ssh.run()

if __name__ == '__main__':
	ip = '127.0.0.1'
	ssh = SSHConnect(dictPath='xx.txt', ip=ip, timeout=0.1, threadNum=10)
	ssh.run()

