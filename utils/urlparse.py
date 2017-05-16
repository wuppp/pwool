# -*- coding:utf-8 -*-

'''
@file: urlparse.py
@author: Roc木木
@time: 17-4-25 下午6:48
'''

import urllib.parse

class urlParse:
	def __init__(self, url):
		self.raw_url = url
		self._parse()

	def _parse(self):
		if 'http://' in self.raw_url or 'https://' in self.raw_url:
			self.url = self.raw_url
		else:
			self.url = 'http://' + self.raw_url

		parse = urllib.parse.urlparse(self.url)
		self.scheme = parse.scheme
		self.netloc = parse.netloc
		self.path = parse.path[:int(parse.path.rfind('/'))+1]
		if self.path == '':
			self.path = '/'
		self.file = parse.path[int(parse.path.rfind('/'))+1:]


if __name__ == '__main__':
	# url = urlParse('www.baidu.com')
	# url = urlParse('http://www.baidu.com')
	# url = urlParse('https://www.baidu.com/')
	# url = urlParse('https://www.baidu.com/index.php')
	url = urlParse('https://www.baidu.com/fuckyou/index.php?id=1&xx=2')
	print(url.url, url.raw_url, url.file, url.path)