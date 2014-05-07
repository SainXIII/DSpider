#!/usr/bin/env python2
#-*- coding:utf-8 -*-

log_spider = logging.getLogger('spider')

class Status(object):
	""
	def __init__(self, threadpool):
		pass

	def currentStatus(self):
		pass

	def display(self):
		t = threading.Thread(target=self.currentStatus)
		t.start()

