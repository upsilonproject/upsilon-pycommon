#!python

import sys

def log(message, level = "INFO"):
    print "[", level, "] ", message

def debug(message = None):
    log(message, "DEBG")

def info(message = None):
    log(message, "INFO")

def warn(message = None):
    log(message, "WARN")

def warning(message = None):
    warn(message)

def error(message = None, e = None):
	log(message, "EROR")

	if not e == None:
		print "Exception:", str(e)

	sys.exit(1)

