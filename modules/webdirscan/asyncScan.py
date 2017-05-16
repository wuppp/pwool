# -*- coding:utf-8 -*-

'''
@file: asyncScan.py
@author: Roc木木
@time: 17-4-25 下午6:46
'''

from urllib import parse as urlparse
import asyncio, aiohttp
import os, sys, argparse

class asyncScan:
	def __init__(self, website, dict_path, concurrentNum=20, retry=3):
		'''
		初始化
		:param website: 目标站点 
		:param dict_path:  字典路径
		:param concurrentNum:  并发数, 默认20
		'''
		self.concurrentNum = concurrentNum
		self.dictionaryPath = dict_path if os.path.isabs(dict_path) else os.path.join(sys.path[0], dict_path)
		tmp = website if 'http://' in website or 'https://' in website else 'http://{url}'.format(url=website)
		self.targetSite = tmp if tmp[-1] == '/' else tmp + '/'
		self.queue = asyncio.Queue()
		self._addQueue()
		self.retryList = {}
		self.maxRetryTime = retry

	def _openDict(self, filename):
		with open(filename) as file:
			for line in file:
				if line.strip() == '':
					continue
				if line.strip()[0] != '#':
					yield line.strip()[1:] if line.strip()[0] == '/' else line.strip()

	def _addQueue(self):
		for each in self._openDict(self.dictionaryPath):
			self.queue.put_nowait(urlparse.urljoin(self.targetSite, each))

	def _isRetry(self, url):
		if url not in self.retryList.keys():
			self.retryList[url] = 1
			return True
		else:
			self.retryList[url] += 1
			if self.retryList[url] > self.maxRetryTime:
				print("[{status}] {url}".format(status='TimeOut', url=url))
				return False

	async def webscan(self):
		while not self.queue.empty():
			url = await self.queue.get()
			# print(url)
			try:
				with aiohttp.Timeout(3):
					async with aiohttp.get(url, allow_redirects=False) as r:
						if r.status == 200:
							print("[{status}] {url}".format(status=r.status, url=url))
			except:
				if self._isRetry(url):
					await self.queue.put(url)

	def run(self):
		loop = asyncio.get_event_loop()
		tasks = [ asyncio.ensure_future(self.webscan()) for _ in range(self.concurrentNum) ]
		loop.run_until_complete(asyncio.gather(*tasks))
		loop.close()

def __usage(arg):
	description = "webscan is a simple web scan tools"
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument("scanUrl", help="the website to be scan", type=str)
	# parser.add_argument("website", help="the website to be scan", type=str)
	parser.add_argument("-d", "--dict", dest="scanDict", help="the dictionary for scan", type=str, default="dict.txt")
	parser.add_argument("-c", "--concurrent", dest="concurrentNum", help="concurrent number", type=int, default=20)
	# add ssh scan
	# parser.add_argument("-s", "--ssh", action='store_true', help="ssh scan", dest="sshScan")
	args = parser.parse_args(arg)
	return args


def dirscan(args):
	# print(args)
	args = __usage(args)
	scan = asyncScan(args.scanUrl, args.scanDict, args.concurrentNum)
	try:
		scan.run()
	except KeyboardInterrupt:
		print('\nExit ...')

if __name__ == '__main__':
	scanner = asyncScan('www.baidu.com', '/home/wp/code/python/webscan/dict/dict.txt')
	scanner.run()