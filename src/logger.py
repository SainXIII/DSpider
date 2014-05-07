#!/usr/bin/env python
#-*- coding:utf-8 -*-

import logging
from logging import config

LOG_FMT = {
	1: {'format': '%(levelname)s %(asctime)s %(message)s'},
	2: {'format': '%(levelname)s %(asctime)s %(name)s %(message)s'},
	3: {'format': '%(levelname)s %(asctime)s %(name)s %(message)s'},
	4: {'format': '%(levelname)s %(asctime)s %(name)s %(thread)d %(threadName)s %(message)s'},
	5: {'format': '%(levelname)s %(asctime)s %(name)s %(thread)d %(threadName)s %(filename)s %(message)s'},
}

LOG_DIC = {
	'version': 1,
	'formatters': {
		'logfile_fmt': {
			'format': '%(levelname)s %(asctime)s %(message)s',
		},
		'display_fmt': {
			'format': '%(levelname)s %(asctime)s %(threadName)s %(message)s',
		}
	},
	"handlers": {
		"logfile_hld": {
			"class": "logging.FileHandler",
			"filename": "spider.log",
			"formatter": "logfile_fmt",
			"level": "DEBUG",
		},
		"display": {
			"class": "logging.StreamHandler",
			"formatter": "display_fmt",
			"level": "DEBUG"
		}
	},

	"loggers": {
		"spider": {
			"level": "DEBUG",
			"handlers": ["logfile_hld", 'display'],
		},
		"term": {
			"level": "INFO",
			"handlers": ["display",],
		},
	},

}


def logger(logfile="spider.log", level=1):
	if not 1 <= level <= 5:
		raise Exception("[args error]: 1 <= level <= 5")
    
	# 根据需求修改配置文件
	LOG_DIC["handlers"]["logfile_hld"]["filename"] = logfile
	# print logging.getLevelName(level*10)
	LOG_DIC["handlers"]["logfile_hld"]["level"] = logging.getLevelName(level*10)
	LOG_DIC["formatters"]["logfile_fmt"] = LOG_FMT[level]
    
	config.dictConfig(LOG_DIC)

