#!/usr/bin/python

#
# Quick & dirty script to find Vorbis files with encoding errors
# potentially caused by https://bugzilla.redhat.com/show_bug.cgi?id=722667
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Copyright (C) 2011 Brian Pepple <bpepple@fedoraproject.org>

import os
import sys
import subprocess

# Run ogginfo on the file and return warning msg.
def vorbisInfo(currdir, f):
	myprocess = subprocess.Popen(['ogginfo',currdir + '/' + f],stdout=subprocess.PIPE)
	(sout,serr) = myprocess.communicate()
	for line in sout.split('\n'):
		if line.strip().startswith('WARNING:'):
			m = line.strip()[len("WARNING:"):].replace("WARNING:"," ") 
			return m

# Walk thru the directory, and pass any vorbis files to be ran with ogginfo.
def findError(currdir):
	print currdir
	for f in os.listdir(currdir):
		path = os.path.join(currdir, f)
		if not os.path.isdir(path):
			if f.endswith('.ogg') or f.endswith('.oga'):
				msg = vorbisInfo(currdir, f)
				if msg:
					print f + ":" + msg
		else:
			findError(path)			

if __name__=='__main__':
	if len(sys.argv) != 2:
		print 'Usage: find_ogg_errors.py directory'
		sys.exit(0)

	findError(sys.argv[1])
