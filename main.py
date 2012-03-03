#!/usr/bin/env python

import sys
import os.path
import random
from pyechonest import config
config.ECHO_NEST_API_KEY = "CVBUZHWXOPIYE6ZRD"

from pyechonest import track

SONG = "TestSongs/We R Who We R/We R Who We R.mp3"

tinfo = track.track_from_filename(SONG)
if tinfo.danceability < 0.5:
	print "Warning: song might not be fun to dance to (danceability {0}%)".format(tinfo.danceability*100)
if tinfo.tempo_confidence < 0.5:
	print "Warning: song tempo might be incorrectly detected, steps might not be on the beat or may gradually become off-beat (confidence {0}%).".format(tinfo.tempo_confidence*100)

print "Dancability:", tinfo.danceability
dir(tinfo)
print "Title:", tinfo

class SMFile:
	def __init__(self, smout):
		self.smout = open(smout, 'w')
		self.smname = smout

	def whl(self, string):
		sys.stdout.write(string + ";\n")
		self.smout.write(string + ";\n")

	def wl(self, string):
		sys.stdout.write(string + "\n")
		self.smout.write(string + "\n")

	def write_header(self, songinfo, fname):
		self.whl("#VERSION:0.81")
		self.whl("#TITLE:{0}".format(songinfo.title))
		self.whl("#SUBTITLE:")
		self.whl("#ARTIST:{0}".format(songinfo.artist))
		self.whl("#MUSIC:{0}".format(os.path.basename(fname)))
		self.whl("#OFFSET:0.000")
		self.whl("#SAMPLESTART:{0}".format(songinfo.end_of_fade_in))
		self.whl("#SAMPLELENGTH:12.000")
		self.whl("#SELECTABLE:yes")
		self.whl("#BPMS:0.000={0}".format(songinfo.tempo))
		self.whl("#TIMESIGNATURES:0.000={0}=4".format(songinfo.time_signature))
		self.whl("#TICKCOUNTS:0.000=4")
		self.whl("#COMBOS:0.000=1")
		self.whl("#SPEEDS:0.000=1=0.000=0")
		self.whl("#SCROLLS:0.000=1.000")
		self.whl("#LABELS:0.000=Song Start")

	def write_notes_header(self, songinfo):
		self.wl("")
		self.wl("//---------------dance-single - Blank----------------")
		self.whl("#NOTEDATA:")
		self.whl("#CHARNAME:")
		self.whl("#STEPSTYPE:dance-single")
		self.whl("#DESCRIPTION:Blank")
		self.whl("#DIFFICULTY:Medium")
		self.whl("#METER:7")
		self.whl("#RADARVALUES:0.199,0.215,0.332,0.005,0.007,217.000,68.000,1.000,0.000,1.000,0.000,0.199,0.215,0.332,0.005,0.007,217.000,68.000,1.000,0.000,1.000,0.000")
		self.whl("#OFFSET:0.000")
		self.whl("#BPMS:0.000={0}".format(songinfo.tempo))
		self.wl("#NOTES:")

def find_bar_length(tinfo):
	barlength = 0.0
	bartotal = 0.0
	for bar in tinfo.bars:
		barlength += bar['duration'] * bar['confidence']
		bartotal += bar['confidence']
	#print "Barlength:", barlength
	#print "Bartotal:", bartotal
	return barlength/bartotal
	
class BarData:
	def __init__(self):
		self.data = []
	
	def set(self, bar, note, value):
		while note > 3:
			bar += 1
			note -= 4
		while len(self.data) <= bar:
			self.data.append(["0000", "0000", "0000", "0000"])
		self.data[bar][note] = value
	
	def write(self, stream):
		i = 0
		for bar in self.data:
			stream.write("// measure {0}\n".format(i))
			for note in bar:
				stream.write(note + "\n")
			if bar is self.data[len(self.data)-1]:
				stream.write(";\n")
			else:
				stream.write(",  ")
			i += 1
	
	def random(self):
		return random.choice(["1000", "0100", "0010", "0001"])

barlen = find_bar_length(tinfo)
bardata = BarData()
bardata.set(1, 3, "0101")

smf = SMFile('TestSongs/We R Who We R/We R Who We R.ssc')
smf.write_header(tinfo, SONG)
smf.write_notes_header(tinfo)

for beat in tinfo.beats:
	#print "Beat {0}".format(beat)
	measure = int(beat['start'] / barlen)
	note = int((((beat['start'] % barlen) / barlen) * 4) + 0.5)
	print "Measure {0}, note {1}".format(measure, note)
	bardata.set(measure, note, bardata.random())

bardata.write(smf.smout)
bardata.write(sys.stdout)
	
print "Duration:", tinfo.duration
print "Average Barlength:", barlen
print tinfo.time_signature