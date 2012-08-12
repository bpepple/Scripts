#!/usr/bin/python

import os
import re
import string

def cleanup_filename(strname):
	(strfile, strext) = os.path.splitext(strname)
	strext = string.strip(strext)
	if strext.lower() == '.cbr' or strext.lower() == '.cbz':
		pattobj = re.compile("\(+(.*)")
		pattobj2 = re.compile("__")
		pattobj3 = re.compile("_")
		name = re.sub(pattobj, "", strfile)
		name = re.sub(pattobj2, " ", name)
		name = re.sub(pattobj3, " ", name)
		return name.rstrip() + strext.lower()
	else:
		return ''

def rename_file(currdir,f):
	c = cleanup_filename(f)
	if (c != "" and c != f):
		print "%s -> %s\n" % (f,c)
		os.rename (currdir + os.sep + f, currdir + os.sep + c)
	return

def process_dir(currdir):
	for f in os.listdir(currdir):
		if not os.path.isdir(f):
			rename_file(currdir, f)
	return

def main():
	process_dir('.')
	return

if __name__=='__main__':
	main()

