#! /usr/bin/python

#
# Script to correct artist & artistsort tags in Ogg Vorbis &
# mp3 files where the artist tag is formatted as "Brown, James" or "Smiths, The"
#
# User needs to have python-eyed3 & python-vorbis installed.
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
# Copyright (C) 2010 Brian Pepple <bpepple@fedoraproject.org>

import os
import sys
import re
import ogg.vorbis
import eyeD3

def cleanup_tag(s):
	# Remove the ([u') & (']) from the vorbis tag
	pattobj1 = re.compile("\[u'")
	pattobj2 = re.compile("'\]")
	tag = re.sub(pattobj1, "", s)
	tag = re.sub(pattobj2, "", tag)
	return tag

def get_original_artist_tag(f):
	vf = ogg.vorbis.VorbisFile(f)
	tag = str(vf.comment().as_dict().get('ARTIST'))
	tag = cleanup_tag(tag)
	return tag

def write_tag(f, artist, sort):
	vf = ogg.vorbis.VorbisFile(f)
	vc = vf.comment()
	nc = ogg.vorbis.VorbisComment()
	for x in vc.items():
		# Don't save the original artist or artistsort
		# tag to prevent any duplicate values
		if x[0] is not ('ARTIST' or 'ARTISTSORT'):
			nc.add_tag(x[0], x[1].encode('utf-8'))
	nc.add_tag('ARTIST', artist)
	nc.add_tag('ARTISTSORT', sort)
	nc.write_to(f)
	
def process_dir(currdir):
	print '[' + currdir + ']'
	for f in os.listdir(currdir):
		path = os.path.join(currdir, f)
		if not os.path.isdir(path):
			if f.endswith('.ogg') or f.endswith('.oga'):
				# Have the original artist tag become the
				# sort tag since I've been consistent in
				# tagging the artist as 'Smiths, The'
				sort_tag = get_original_artist_tag(path)
				s = sort_tag
				line = s.split(', ')
				try:
					artist_tag = line[1] + " " + line[0]
					write_tag(path, artist_tag, sort_tag)
					print 'File: %s | Artist: %s | Sort: %s' % (f, artist_tag, sort_tag)
				except IndexError:
					print "File: %s does not need to be fixed. " % (f)
			if f.endswith('.mp3'):
				tag = eyeD3.Tag()
				tag.link(path)
				s = tag.getArtist()
				line = s.split(', ')
				try:
					new_artist = line[1] + " " + line[0]
					tag.setArtist(new_artist)
					tag.setTextFrame("TSOP", str(s))
					tag.update()
					print "File: %s | Artist: %s | Sort: %s" % (f, new_artist, s)
				except IndexError:
					print "File: %s does not need to be fixed. " % (f)
		else:
			process_dir(path)

if __name__=='__main__':
	if len(sys.argv) != 2:
		print 'Usage: sort_artist_fix.py directory'
		sys.exit(0)

	process_dir(sys.argv[1])
