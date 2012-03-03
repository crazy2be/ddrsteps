#!/usr/bin/env python

from pyechotest import config
config.ECHO_NEST_API_KEY = "CVBUZHWXOPIYE6ZRD"

from pyechotest import track

tinfo = track.upload(url="TestSongs/We R Who We R/We R Who We R.mp3")