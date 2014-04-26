#!/usr/bin/env python
#-*- coding:utf-8 -*-

import chardet

def x2Unicode(d, charset=None):
	udata = ''
	if isinstance(d, str):
		if not charset:
			try:
				charset = chardet.detect(d).get('encoding')
			except:
				pass
		if charset:
			udata = d.decode(charset, 'ignore')
		else:
			udata = d
	else:
		udata = d

	return udata
	
