#!/usr/bin/env python
#-*- coding:utf-8 -*-

from data import UrlObject
from utils import x2Unicode
from parser import Webkit, StaticAnalyzer
from threadpool import Thread, Threadpool

import urlparse
import Queue
import requests
import os

class Fetcher(object):
	""
	def __init__(self, header={}, maxlen=2*20):
		self.maxlen = maxlen
		self.header = header

	def fetch(self, urlobj):
		req = requests.get(urlobj.url, headers=self.header)
		
		if req.headers.get('content-type').find('text/html') == -1:
			print req.headers.get('content-type')
			print 'type is note text/html'
			return u''
		length = req.headers.get('content-length')
		if length and (int(length) > self.maxlen):
			return u''
		if req.content:
			html = x2Unicode(req.content)
			return html
		return u''
			
class Spider(object):
	""
	def __init__(self, threads, depth=0, crawl_tags=[], ignore=[], cum_headers={}, dynamic_parse=False):
		self.task_queue = Queue.Queue()
		self.link_cache = []
		self.max_threads = threads
		self.depth = depth
		self.headers = cum_headers
		self.maxlen = 2**30
		self.crawl_tags = crawl_tags
		self.ignore_suff = ignore
		self.dynamic_parse = dynamic_parse
		if self.dynamic_parse:
			self.engine = Webkit()
		else:
			self.engine = StaticAnalyzer()

	def start(self, url):
		url = x2Unicode(url)
		urlobj = UrlObject(url)

		u = urlparse.urlparse(url)
		self.origin = (u.scheme, u.netloc)
		
		self.task_queue.put(urlobj)

	def run(self):
		threadpool = Threadpool(self.work, max_htreads=self.max_threads, thread=Thread, queue=self.task_queue)
		threadpool.add(self.task_queue.get())
		threadpool.join()

	def work(self, urlobj):
		fetcher = Fetcher()
		html = fetcher.fetch(urlobj)
		if html is '':
			return None
		urlobj.html = html				
		urlobjs = craw(urlobj)
		return urlobjs
		
	def crawl(self, urlobj):
		depth = urlobj.depth+1
		urls = []
		if depth > self.depth:
			return None
		if self.dynamic_parse:
			llink = self.engine.get_links(urlobj.url)
		else:
			llink = self.engine.get_links(urlobj.html, urlobj.url, self.crawl_tags)
		for link in llink:
			link = x2Unicode(link)
			if not self.check_url(link):
				continue
			self.link_cache.append(link)
			urlobj = UrlObject(link, depth=depth)
			urls.append(urlobj)
		#print self.link_cache
		return urls
	
	def check_url(self, link):
		if link in self.link_cache:
			return False
		if not self.check_origin(link):
			return False
		link_ext = os.path.splitext(urlparse.urlsplit(link).path)[-1][1:]
		if link_ext in self.ignore_suff:
			return False
		return True

	def check_origin(self, link):
		u = urlparse.urlparse(link)
		if (u.scheme, u.netloc) == self.origin:
			return True
		return False

if __name__ == '__main__':		
	human_headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36',
					 'Accept-Encoding':'gzip,deflate,sdch'}

	crawl_tags = ['a', 'base', 'iframe', 'frame', 'object']
	ignore = ['js','css','png','jpg','gif','bmp','svg','exif','jpeg','exe','rar','zip']
	spider = Spider(0, depth=2, crawl_tags=crawl_tags, ignore=ignore)
	spider.start('http://it.ouc.edu.cn')
	spider.run()
