#!/usr/bin/env python
#-*- coding:utf-8 -*-

from splinter import Browser
import lxml.html
import urlparse

class Webkit(object):
	""
	def __init__(self):
		self.tag_attr = {
			'*': 'href',
			'frame': 'src',
			'iframe': 'src',
			'object': 'src'
		}

	def get_links(self, url):
		links = []
		self.browser = Browser('phantomjs')
		self.browser.visit(url)
		for tag, attr in self.tag_attr.viewitems():
			llinks = self.browser.find_by_xpath('//%s[@%s]'% (tag, attr))
			if not llinks:
				continue
			for link in llinks:
				link = link.__getitem__(attr)
				if not link:
					continue
				if link == 'about:blank' or link.startswith('javascript:'):
					continue
				if not link.startswith('http:'):
					link = urlparse.urljoin(url, link)
				links.append(link)

		return links
			
	def close(self):
		self.browser.quit()
	

class StaticAnalyzer(object):
	""
	@staticmethod
	def get_links(html, base_url, tags = []):
		links = []
		tags = tags
		html = lxml.html.document_fromstring(html)
		html.make_links_absolute(base_url)
		links_html = html.iterlinks()
		links = [ x[2] for x in links_html if x[0].tag in tags ]
		return links

if __name__ == '__main__':
	import requests
	html = requests.get('http://it.ouc.edu.cn').content
	a = StaticAnalyzer()
	print a.get_links(html, 'http://it.ouc.edu.cn', ['a', 'iframe'])
	#a = Webkit()
	#print a.get_links('http://it.ouc.edu.cn')
