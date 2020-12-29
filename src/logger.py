#!python

import sys

def log(args, level = "INFO"):
	print("[", level, "]", end=' ')

	if type(args) == str:
		print(args, end=' ')
	else: 
		for o in args:
			print(str(o), end=' ')
				
	print()

def debug(*args):
	log(args, "DEBG")

def info(*args):
	log(args, "INFO")

def warn(*args):
	log(args, "WARN")

def warning(*args):
	warn(args)

def error(*args):
	log(args, "EROR")

	sys.exit(1)

