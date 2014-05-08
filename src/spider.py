#!/usr/bin/env python
#-*- coding:utf-8 -*-

from data import UrlObject
from utils import x2Unicode
from parser import Webkit, StaticAnalyzer
from threadpool import Thread, Threadpool
import logger

import logging
import urlparse
import Queue
import requests
import os

log_spider = logging.getLogger('spider')

class Fetcher(object):
	""
	def __init__(self, header={}, maxlen=2**30):
		self.maxlen = maxlen
		self.header = header

	def fetch(self, urlobj):
		req = requests.get(urlobj.url, headers=self.header)
		
		if req.status_code > 400:
			log_spider.debug('visit %s page error(%d)' % (req.url, req.status_code))
			return u''
		if req.headers.get('content-type').find('text/html') == -1:
			log_spider.debug('Content-Type is not text/tml(%s)' % req.headers.get('content-type'))
			return u''
		length = req.headers.get('content-length')
		if length and (int(length) > self.maxlen):
			log_spider.debug('Content is to long(%s)' % length)
			return u''
		if req.content:
			html = x2Unicode(req.content)
			return html
		return u''
			
class Spider(object):
	""
	def __init__(self, threads, depth=0, crawl_tags=[], ignore=[], cum_headers={}, dynamic_parse=False):
		self.site = ''
		#self.task_queue = Queue.Queue()
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
		self.site = url
		urlobj = UrlObject(url)

		u = urlparse.urlparse(url)
		self.origin = (u.scheme, u.netloc)
		threadpool = Threadpool(self.work, max_threads=self.max_threads, thread=Thread)
		threadpool.add([urlobj,])
		threadpool.join()

	def work(self, urlobj):
		fetcher = Fetcher()
		html = fetcher.fetch(urlobj)
		if html is u'':
			return None
		urlobj.html = html				
		urlobjs = self.crawl(urlobj)
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
			link = self.unify_url(link)
			link = x2Unicode(link)
			if not self.check_url(link):
				continue
			self.link_cache.append(link)
			urlobj = UrlObject(link, depth=depth)
			urls.append(urlobj)
		return urls
	
	def unify_url(self, link):
		url = link.strip()
		url = url.split('#')[0]

		return url
	
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
	import sys
	human_headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36',
					 'Accept-Encoding':'gzip,deflate,sdch'}

	crawl_tags = ['a', 'base', 'iframe', 'frame', 'object']
	ignore = ['js','css','png','jpg','gif','bmp','svg','exif','jpeg','exe','rar','zip', 'doc']
	spider = Spider(10, depth=20, crawl_tags=crawl_tags, ignore=ignore, cum_headers=human_headers)
	logger.logger()
	spider.start(sys.argv[1])

