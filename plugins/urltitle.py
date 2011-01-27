# -*- coding: utf-8 -*-
import re, urllib2

from mongoengine import connect

import settings
from plugins import Plugin, command
from plugins.urllogger.models import URLLog
from utils import filesize


if settings.DB_NAME:
    connect(settings.DB_NAME)

_ext = getattr(settings, 'URL_SIZE_EXTENSIONS', None)

class URLTitle(Plugin):

    def on_privmsg(self, irc, prefix, params):
        channel = params[0]
        msg = params[-1]

        if re.search('(http://open\.spotify\.com/)(album|artist|track)/([^\s$]+)', msg): return
        m = re.findall('(-?)(https?://[^\s$]+)+', msg)
        if m:
            for url in m:
                if url[0]: # Skip all url's with a leading dash
                    continue
                if len(m) > 1:
                    irc.msg(channel, '{0} [ {1} ]'.format(self.call(url[1]), url[1]))
                else:
                    irc.msg(channel, '{0}'.format(self.call(url[1]), url[1]))
        return


    @command
    def title(self, search=None):
        """Fetches the latest url and returns the responding title. Can do easy searches á la `!title gfu` to fetch the latest url containing the word 'gfu'"""
        try:
            if search:
                u = URLLog.objects(url__contains=search).order_by('-last_post').first()
            else:
                u = URLLog.objects.order_by('-last_post').first()
        except URLLog.DoesNotExist:
            return 'Could not find any matching URL\'s'

        return self.call(u.url, True)


    def call(self, url, error=False):
        data = urllib2.urlopen(url)
        info = data.info()

        if info['content-type'].split('/', 1)[0] == 'text':
            m = re.search('<title[^>]*>([^<]*)</title>', data.read())
            if m:
                title = m.group(1).strip().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                title = re.sub('[ ]{2,}', ' ', title)
                
                if title:
                    return '» {0} [ {1} ]'.format(title, url)

        elif _ext:
            ext = url.rsplit('.', 1)[1]
            if ext in _ext:
                return '» Content-type: {0} [{1}]'.format(info['content-type'], filesize(info['content-length']))

        return 'Could not fetch title for {0}'.format(url) if error else ''
