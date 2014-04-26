#!/usr/bin/env python
#-*- coding:utf-8 -*-


class UrlObject(object):
	""
	def __init__(self, url, html=None, depth=0):
		self.url = url
		self.html = html
		self.depth = depth
		self.params = {}
		self.post_data = {}
		self.fragments = {}
	
	def __str__(self):
		return self.url

	def __repr__(self):
		return '<Url object: %s>' % self.url

	def __hash__(self):
		return hash(self.url)


