#!python

def log(message, level = "INFO"):
    print "[", level, "] ", message

def error(message = None, e = None):
	log(message, "ERROR")

	if not e == None:
		print "Exception:", str(e)

	sys.exit(1)

