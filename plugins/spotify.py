# -*- coding: utf-8 -*-
import re, urllib2, time
import xml.etree.cElementTree as tree

from plugins import Plugin

class Spotify(Plugin):

    apiurl = "http://ws.spotify.com/lookup/"
    apiversion = '1'

    def timeconversion(self, seconds):
        format = '%H:%M:%S'
        if seconds < 3600:
            format = format[3:]
        return time.strftime(format, time.gmtime(seconds))
        

    def on_privmsg(self, irc, prefix, params):
        channel = params[0]
        msg = params[-1]

        m = re.match('(http://open\.spotify\.com/|spotify:)(album|artist|track)[:/]([^\s$]+)', msg)

        if not m:
            return
        uri = 'spotify:{}:{}'.format(m.group(2), m.group(3))
        data = self.call(uri)
        xml = tree.fromstring(data)

        if m.group(2) == 'album':
            ret = "{0} [{1}] » {2}".format(xml[1][0].text, xml[0].text, uri)
        elif m.group(2) == 'track':
            ret = "{0} - {1} [{2}] ({3}) » {4}".format(xml[1][0].text, xml[0].text, xml[2][0].text, self.timeconversion(float(xml[6].text)), uri)
        elif m.group(2) == 'artist':
            ret = "{0} » {1}".format(xml[0].text, uri)

        irc.msg(channel, ret)


    def call(self, uri):
        url = ''.join([self.apiurl, self.apiversion, '/?uri=', uri])
        data = urllib2.urlopen(url).read()

        return data
