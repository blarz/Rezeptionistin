#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import logging
from asyncirc.ircbot import IRCBot
import sys
import socket
import re
import urllib2
from bs4 import BeautifulSoup

server="irc.freenode.net"
port=6667
nick="Rezeptionistin"
ircchan="#k4cg"

if sys.hexversion > 0x03000000:
    raw_input = input

logging.basicConfig(level=logging.DEBUG)
irc = IRCBot(server, port, nick)

# Custom Functions
def netcat(hostname, port, content):
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.shutdown(socket.SHUT_WR)
    while 1:
        data = s.recv(1024)
        if data == "":
            break
        f = data
    s.close()
    return f

def geturltitle(message):
    try:
        url = re.search("(?P<url>https?://[^\s]+)", message).group("url")
        soup = BeautifulSoup(urllib2.urlopen(url))
        t = soup.title.string
    except:
        t = "Was zur Hoelle... Check ich nicht."
    return t.encode('ascii','ignore')


# IRC Handlers
@irc.on_join
def on_join(self, nick, host, channel):
    self.msg("#" + channel, ':Ich war nur kurz weg. Aber hier bin ich wieder.')

@irc.on_msg
def on_msg(self, nick, host, channel, message):
    if message.lower().startswith('!help'):
        self.msg(nick, ":Erzaehl mir doch was du brauchst, mein Junge.")
        self.msg(nick, ":Ich kann bisher:")
        self.msg(nick, ":!kt - Zeige aktuelle Temperatur in der K4CG.")
        self.msg(nick, ":!gt - Guten Tag wuenschen.")
        self.msg(nick, ":!np - Dir sagen welche Musik so laeuft.")
        self.msg(nick, ":oder dir den Titel von URLs sagen die du in den Channel postest")
    if message.lower().startswith('!kt'):
        temp = netcat("2001:a60:f073:0:21a:92ff:fe50:bdfc", 31337, "9001")
        self.msg(channel, ':Die aktuelle Temeratur in der K4CG ist{temp} Grad'.format(temp=temp) )
    if message.lower().startswith('!gt'):
        self.msg(channel, ':Ach halts Maul.')
    if message.lower().startswith('!np'):
        self.msg(channel, ':Das funktioniert noch nicht.')
    if message.startswith('http://'):
        title = geturltitle(message)
        self.msg(channel, ":{title}".format(title=title))
    if message.startswith('https://'):
        title = geturltitle(message)
        self.msg(channel, ":{title}".format(title=title))

# Start Bot
irc.start()
irc.join(ircchan)

# Run Eventloop
try:
    while irc.running:
        irc.send_raw(raw_input(""))
except KeyboardInterrupt:
    print("Received exit command")
finally:
    irc.stop()
