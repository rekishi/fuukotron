#!/usr/bin/env python3

"""
fuuko-chan, Megatron's slave
"""

import irc.bot
import irc.strings
import random
import json
import requests
import urllib.request
import html
import types
import socket
import sys
import signal
import subprocess
import re
from html.parser import HTMLParser
import urllib.parse
from time import strftime
from irc.client import ServerConnection,ip_numstr_to_quad, ip_quad_to_numstr
#from cloudbot import hook
random.seed()

def privmsg(self,target, text):
	try:
		self.send_raw("PRIVMSG %s :%s" % (target, text))
	except:
		self.send_raw("PRIVMSG %s :%s" % (target, text[:490]))
		self.privmsg(target,text[490:])

class URLReader(HTMLParser):
	def handle_starttag(self,tag,attrs):
		if tag.lower() == 'title':
			self.title = True
	def handle_data(self,data):
		if self.title == True:
			self.title = data
"""
not implemented
class Points():
	def __init__(self):
		self.load()
	def load(self):
		pfile = open('/home/pi/fuko-chan/points.txt','r+')
		self.d = {}
		for pointpair in qfile:
			self.d[pointpair.split(',')[0]] = int(pointpair.split(',')[1])
		pfile.truncate()
		for nick,points in self.d.items():
			pfile.write(nick+','+str(points)+'\n')
		pfile.close()
	def add(self,nick):
		pfile = open('/home/pi/fuko-chan/points.txt','a')
		if nick not in self.d.keys():
			self.d[nick] = 0
		self.d[nick] += 1
		pfile.write(nick+','+str(self.d[nick])+'\n')
		pfile.close()
	def rm(self,nick):
		pfile = open('/home/pi/fuko-chan/points.txt','a')
		if nick not in self.d.keys():
			self.d[nick] = 0
		self.d[nick] -= 1
		pfile.write(nick+','+str(self.d[nick])+'\n')
		pfile.close()
	def scoreboard(self):
		scores = 'LEADERBOARD:::   '
		c = 0
		for nick,points in sorted(self.d.items(),key=lambda element:element[1],reverse=True):
			if c > 9:
				break
			scores += nick+': '+str(points)+' | '
			c += 1
		scores = scores[:-3]
		return scores
"""
"""
class Translate():
	def goog_trans(api_key, text, source, target):
		url = 'https://www.googleapis.com/language/translate/v2'

		if len(text) > max_length:
			return "This command only supports input of less then 100 characters."

		params = {
		'q': text,
		'key': api_key,
		'target': target,
		'format': 'text'
		}

		if source:
			params['source'] = source

		request = requests.get(url, params=params)
		parsed = request.json()

		if parsed.get('error'):
			if parsed['error']['code'] == 403:
				return "The Translate API is off in the Google Developers Console."
			else:
				return "Google API error."

		if not source:
			return '(%(detectedSourceLanguage)s) %(translatedText)s' % (parsed['data']['translations'][0])
		return '%(translatedText)s' % parsed['data']['translations'][0]


	def match_language(fragment):
		fragment = fragment.lower()
		for short, _ in lang_pairs:
			if fragment in short.lower().split():
				return short.split()[0]

		for short, full in lang_pairs:
			if fragment in full.lower():
				return short.split()[0]

		return None


	@hook.command()
	def translate(text, bot):
#		[source language [target language]] <sentence> - translates <sentence> from source language (default autodetect)
#		 to target language (default English) using Google Translate
#
		api_key = bot.config.get("api_keys", {}).get("google_dev_key", None)
		if not api_key:
			return "This command requires a Google Developers Console API key."


		args = text.split(' ', 2)


		try:
			if len(args) >= 2:
				sl = match_language(args[0])
				if not sl:
					return goog_trans(api_key, text, '', 'en')
				if len(args) == 2:
					return goog_trans(api_key, args[1], sl, 'en')
				if len(args) >= 3:
					tl = match_language(args[1])
				if not tl:
					if sl == 'en':
						return 'unable to determine desired target language'
					return goog_trans(api_key, args[1] + ' ' + args[2], sl, 'en')
				return goog_trans(api_key, args[2], sl, tl)
			return goog_trans(api_key, text, '', 'en')
		except IOError as e:
			return e


	lang_pairs = [	
		("no", "Norwegian"),
		("it", "Italian"),
		("ht", "Haitian Creole"),
		("af", "Afrikaans"),
		("sq", "Albanian"),
		("ar", "Arabic"),
		("hy", "Armenian"),
		("az", "Azerbaijani"),
		("eu", "Basque"),
		("be", "Belarusian"),
		("bg", "Bulgarian"),
		("ca", "Catalan"),
		("zh-CN zh", "Chinese"),
		("hr", "Croatian"),
		("cs", "Czech"),
		("da", "Danish"),
		("nl", "Dutch"),
		("en", "English"),
		("et", "Estonian"),
		("tl", "Filipino"),
		("fi", "Finnish"),
		("fr", "French"),
		("gl", "Galician"),
		("ka", "Georgian"),
		("de", "German"),
		("el", "Greek"),
		("ht", "Haitian Creole"),
		("iw", "Hebrew"),
		("hi", "Hindi"),
		("hu", "Hungarian"),
		("is", "Icelandic"),
		("id", "Indonesian"),
		("ga", "Irish"),
		("it", "Italian"),	
		("ja jp jpn", "Japanese"),
		("ko", "Korean"),
		("lv", "Latvian"),
		("lt", "Lithuanian"),
		("mk", "Macedonian"),
		("ms", "Malay"),
		("mt", "Maltese"),	
		("no", "Norwegian"),
		("fa", "Persian"),
		("pl", "Polish"),
		("pt", "Portuguese"),
		("ro", "Romanian"),
		("ru", "Russian"),
		("sr", "Serbian"),
		("sk", "Slovak"),
		("sl", "Slovenian"),
		("es", "Spanish"),
		("sw", "Swahili"),
		("sv", "Swedish"),
		("th", "Thai"),
		("tr", "Turkish"),
		("uk", "Ukrainian"),
		("ur", "Urdu"),
		("vi", "Vietnamese"),
		("cy", "Welsh"),
		("yi", "Yiddish")
	]
"""
class Quotes():
	def __init__(self):
		self.load()
	def load(self):
		qfile = open('/home/pi/fuko-chan/quotes.txt')
		self.d = []
		for quote in qfile:
			self.d += [quote]
	def add(self,art):
		qfile = open('/home/pi/fuko-chan/quotes.txt','a')
		qfile.write(art+'\n')
		qfile.close()
		self.load()
	def get(self,n):
		try:
			return self.d[n].strip('\n')
		except IndexError:
			return None
	def random(self):
		n = random.randrange(len(self.d))
		return (n,self.d[n].strip('\n'))
	

class Queue():
	def __init__(self,l):
		self.d = []
		self.l = l
	
	def push(self,e):
		self.d += [e]
		if len(self.d) > self.l:
			self.d.pop(0)
	def search(self,e):
		if e in self.d:
			return True
		return False

class Aliases():
	def __init__(self):
		self.load()
	def load(self):
		self.d = []
		afile = open('/home/pi/fuko-chan/aliases.txt','r')
		for aliases in afile:
			aliases = aliases.strip().split(',')
			try:
				while 1:
					aliases.remove('')
			except ValueError:
				self.d += [aliases]

	def get(self,nick):
		for alias in self.d:
			if nick.lower() in alias:
				return alias
		return []

	def add(self,new,old=None):
		if not old:
			if self.get(new) == []:
				afile = open('/home/pi/fuko-chan/aliases.txt','a')
				afile.write(new.lower()+',\n')
				afile.close()
				self.load()
		else:
			if self.get(new) == []:
				afile = open('/home/pi/fuko-chan/aliases.txt','r')
				d_afile = afile.readlines()
				afile.close()
				afile = open('/home/pi/fuko-chan/aliases.txt','w')
				for aliases in d_afile:
					aliases = aliases.strip().split(',')
					try:
						while 1:
							aliases.remove('')
					except ValueError:
						if old.lower() in aliases:
							aliases += [new.strip(',').lower()]
						afile.write(','.join(aliases)+'\n')
				afile.close()
				self.load()


class Tells():
	def __init__(self):
		self.d = {}
		self.aliases = Aliases()
		self.load()

	def load(self):
		tfile = open('/home/pi/fuko-chan/tells.txt','r')
		tmpd = {}
		for line in tfile:
			tmpline = line.strip('\n').split(';',maxsplit=3)
			try:
				tmpd[tmpline[0]] += [(tmpline[1],tmpline[3],tmpline[2])]
			except KeyError:
				tmpd[tmpline[0]] = [(tmpline[1],tmpline[3],tmpline[2])]

		tfile.close()
		self.d = tmpd

	def save(self):
		tfile = open('/home/pi/fuko-chan/tells.txt','w')
		tfile.truncate()
		for dsts in self.d.items():
			for tells in dsts[1]:
				tfile.write(dsts[0]+';'+tells[0]+';'+tells[2]+';'+tells[1]+'\n')
		tfile.close()

	def add(self,dst,src,msg):
		try:
			self.d[dst] += [(src,msg,strftime('%a %b %d, %I:%M %p %Z'))]
		except KeyError:
			self.d[dst] = [(src,msg,strftime('%a %b %d, %I:%M %p %Z'))]
		self.save()
		self.load()

	def get(self,dst):
		pos_aliases = self.aliases.get(dst)
		for alias in pos_aliases:
			try:
				ret = self.d[alias]
				del self.d[alias]
				self.save()
				self.load()
				return ret
			except KeyError:
				pass
		return None

	
	def dump(self):
		return self.d.items()
	
	def dsts(self):
		ret = []
		for nick in self.d.keys():
			ret += self.aliases.get(nick)
		return ret

class fuukochan(irc.bot.SingleServerIRCBot):
	def __init__(self, channel, nickname, server, port=6667):
		irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
		self.connection.privmsg = types.MethodType(privmsg,self.connection)
		self.channel = channel
		self.nname = nickname
		self.lstmsgs = Queue(15)
		self.tells = Tells()
		self.quotes = Quotes()
		jfile = open('/home/pi/fuko-chan/johns.txt','r')
		self.johns = []
		for john in jfile:
			self.johns += [john.strip()]
		jfile.close()
		

	


	
	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + "_")

	def on_welcome(self, c, e):
		c.privmsg('nickserv','identify starfish')
		c.join(self.channel)
		c.names(self.channel)

	def on_kick(self, c, e):
		c.join(self.channel)
		c.privmsg(self.channel,'ok im sory pls dont hurt me i wont do it agin promis')
	def on_namreply(self,c,e):
		pos_new_nicks = e.arguments[2].split(' ')
		try:
			while 1:
				pos_new_nicks.remove('')
		except ValueError:
			pos_new_nicks = [nick.strip('@+&~%') for nick in pos_new_nicks]
		for nick in pos_new_nicks:
			self.tells.aliases.add(nick,old=None)

	def on_join(self,c,e):
		self.tells.aliases.add(e.source.nick,old=None)

	def on_nick(self,c,e):
		self.tells.aliases.add(e.target,old=e.source.nick)

	def on_pubmsg(self, c, e):
		m = e.arguments[0]
		srcnick = e.source.nick
		if e.source.nick == 'orc':
			pass
		if srcnick == 'NUMC' or srcnick == 'NUMC-mod':
			try:
				if 'joined the game' in m:
					self.tells.aliases.add(m.split()[0],old=None)
				srcnick = m[1:].split('>')[0]
				m = m.split('>',maxsplit=1)[1][1:]
			except IndexError:
				pass
		sed = m.split('/')
		for url in m.split():
			try:
				if 'http://' in url or 'https://' in url:
					h_b = requests.head(url,headers={'user-agent':'Mozilla/5.0 ;Windows NT 6.1; WOW64; Trident/7.0; rv:11.0; like Gecko'})
					if 'text/html' not in h_b.headers['content-type']:
						c.privmsg(self.channel,'content-type: '+h_b.headers['content-type'])
						raise
					b = requests.get(url,headers={'user-agent':'Mozilla/5.0 ;Windows NT 6.1; WOW64; Trident/7.0; rv:11.0; like Gecko'})
					infourl = URLReader()
					infourl.title = False
					infourl.feed( b.text)
					if infourl.title:
						c.privmsg(self.channel,infourl.title+' - '+url)
						c.privmsg(self.channel,self.think(infourl.title.lower()))
			except:
				pass
		if srcnick.lower() in self.tells.dsts():
			for tell in self.tells.get(srcnick.lower()):
				c.privmsg(self.channel,srcnick+': '+tell[0]+' said "'+tell[1]+'" on '+tell[2])
#its fuggin broke
		if m[:2] == '.gkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk':
			try:
				num = int(m[2:].split(' ',maxsplit=1)[0])-1
			except:
				num = 0
			try:
				query = m.split(' ',maxsplit=1)[1]
			except IndexError:
				c.privmsg(self.channel,'usage: .g <search term> OR .g[result number] <search term> (default first result)')
				return
			results = json.loads(urllib.request.urlopen('https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q='+urllib.parse.quote(query)).read().decode('utf8'))
			try:
				c.privmsg(self.channel,html.unescape(results['responseData']['results'][num]['titleNoFormatting'])+' ('+urllib.parse.unquote(results['responseData']['results'][num]['url'])+')')
			except IndexError:
				c.privmsg(self.channel,'no result #'+str(num+1)+' found for '+query)
		if m[:6] == '.tell ':
			try:
				dstnick = m[6:].split(' ',maxsplit=1)[0].lower()
				dstmsg =  m[6:].split(' ',maxsplit=1)[1]
				if dstnick == '!dump':
					c.privmsg(self.channel,srcnick+': I am messaging you what everyone has told me in recent memory.')
					for tell in self.tells.dump():
						for tmsg in tell[1]:
							c.privmsg(srcnick,tmsg[0]+' told '+tell[0]+' "'+tmsg[1]+'" on '+tmsg[2])
				elif dstnick == self.nname:
					c.privmsg(self.channel,'B-but I\'m right here ;_;')
				elif dstnick in self.tells.aliases.get(srcnick):
					c.privmsg(self.channel,'You can tell yourself that.')
				elif dstnick.strip():
					self.tells.add(dstnick,srcnick.lower(),dstmsg)
					c.privmsg(self.channel,srcnick+': I\'ll tell '+dstnick+' that when I see them.')
			except:
				c.privmsg(self.channel,'usage: .tell <person> <message> (user will be notified of your message next time they speak)')
		elif m[:10] == '.rlaliases':
			if srcnick == 'rekishi':
				try:
					self.tells.aliases.load()
					c.privmsg(self.channel,'Aliases reloaded!')
				except:
					c.privmsg(self.channel,'Aliases reloading failed.  Reason: rekishi fucked up')
			else:
				c.privmsg(self.channel,'Aliases reloading failed.  Reason: U ARNET AUTHORZIED, SCURB!!!!!! XDD')

		elif m[:7] == '.alias ':
			try:
				if m[7:]:
					self.tells.aliases.add(m[7:],old=srcnick)
					c.privmsg(self.channel,srcnick+': added an alternative nick for you: '+m[7:])
			except:
				c.privmsg(self.channel,'usage: .alias <alternative name> (used by '+self.nname+' to identif you when someone uses \'.tell\')')
		elif m[:6] == '.quote':
			try:
				n = int(m[6:])
				if n <= 0:
					raise ValueError
				try:
					c.privmsg(self.channel,"quote "+str(n)+" of "+str(len(self.quotes.d))+": "+self.quotes.get(n-1))
				except TypeError:
					c.privmsg(self.channel,"quote "+str(n)+" not found.")
			except ValueError:
				ranquote = self.quotes.random()
				c.privmsg(self.channel,"quote "+str(ranquote[0]+1)+" of "+str(len(self.quotes.d))+": "+ranquote[1])
		elif m[:10] == '.addquote ':
			self.quotes.add(m[10:])
			c.privmsg(self.channel,srcnick+": quote added.")
				
		elif sed[0] == 's' and len(sed) == 3:
			rm = ''
			for msg in reversed(self.lstmsgs.d):
				if sed[1] in msg[1]:
					c.privmsg(self.channel,msg[0]+' meant to say: '+msg[1].replace(sed[1],sed[2]))
					rm = (msg[0],msg[1])
					break
			try:
				self.lstmsgs.d.remove(rm)
			except ValueError:
				c.privmsg(self.channel,'usage: s/<oldstring>/<newstring> (replace oldstring with newstring from previous messages, used for correcting messages)')
			
		else:
			if m:
				self.lstmsgs.push((srcnick,m))
			if 'moonman' in m.lower():
				c.privmsg(self.channel, 'MOONMAN MOONMAN CAN\'T YOU SEE! SPICS AND NIGGERS NEED TO HANG FROM TREES!')
			if 'edgy' in m.lower():
				c.privmsg(self.channel, 'y are you so edgy')
			if 'fort kickass' in m.lower():
				c.privmsg(self.channel, 'your authority is not recognized')
			if 'gay' in m.lower():
				c.privmsg(self.channel, 'im gay')
			if '.help' in m.lower():
				c.privmsg(self.channel, '.tell to leave a message for a user, .addquote to add quote, .quote to replay quote, .alias to add alias')
		#	if 'mzmz farts' in m.lower():
		#		c.privmsg(self.channel, 'fucking cuck')
			if 'dank' in m.lower():
				c.privmsg(self.channel, '3meme5me')
			if m[:2] == 'up':
				c.privmsg(self.channel, m+'\'d bro!!!!!!')
			if 'waifu' in m.lower():
				c.privmsg(self.channel, srcnick+'\'s waifu is shit')
			if  'fuukochan' in m.lower():
				c.privmsg(self.channel,'have a starfish '+srcnick)
			if '.fedoratip' in m.lower():
				c.privmsg(self.channel,'m\''+srcnick)
			if 'ayy' in m.lower() and 'ayypot' not in m:
				c.privmsg(self.channel,'lmao')
			if 'tumblr' in m.lower():
				c.privmsg(self.channel, srcnick+', fuck off normie!')
			if 'beanerino' in m.lower():
				c.privmsg(self.channel,'BEANERINO'+'!'*(16+random.randrange(24)))
		#	if 'koala' in m.lower() or 'wsu' in m.lower() or 'wichita state' in m.lower():
		#		c.privmsg(self.channel,'SHUT THE FUCK UP FAGGOT')
		#	if 'jess' in m.lower():
		#		c.privmsg(self.channel, 'who?')
			if 'hate' in m.lower() and 'meme' in m.lower():
				c.privmsg(self.channel,srcnick+': um what did u just say about memes???? il have u no that mems rr the BEST things isnce al gore invented the sieries of tubes and without mems i would be VEry hurt all the tim n probly cry 2slep evry nite so BACK OFF THE MMEES YA DIP cuz consequpences will NEVR BE THE SAME >:(((((((')
#			if 'rekishi' in m.lower():
#				c.privmsg(self.channel,'I love my Master')
			if 'doom' in m.lower():
				c.privmsg(self.channel,'YOU BETTER WATCH OUT '+srcnick+' CUZ MR DOOM IS GONA BEET YOU IN SMASH WITH HIS SIGATURE DOOMSDI(tm)(r)(c) STOP PLAYING SMASH YOU CASUAL')
			if 'pit' in m.lower():
				c.privmsg(self.channel,'i completely agree that Pit should be banned from competitive play')
			if ':^)' in m:
				c.privmsg(self.channel,'(^:')
			if 'rip' in m:
				c.privmsg(self.channel,'RIIIIIIIIP')
			if 'sniffin' in m:
				c.privmsg(self.channel,'sniffin and dickin mayn')
			if '(^:' in m:
				c.privmsg(self.channel,':^)')
#			if 'john' in m.lower():
#				c.privmsg(self.channel,'so you suck at smash today because '+self.johns[random.randrange(len(self.johns))]+'?')
			if m[-4:] == 'boys':
				c.privmsg(self.channel,' '.join(list(m)).upper())
			if 'lol' in m.lower() and 'loli' not in m or 'LOL' in m.lower() and 'loli' not in m:
				c.privmsg(self.channel,'LOL'+'!'*(16+random.randrange(24)))
			if m == 'holy shit':
				c.privmsg(self.channel,'HOLY SHIT '+srcnick.upper())
			if m[0] == '[' and m[-1] == ']':
				intense = m[1:-1]
				c.privmsg(self.channel,'['+intense.upper()+' INTENSIFIES]')
			if m == ' '.join(list(''.join(m.split()))) and m.upper() == m:
				cross = list(''.join(m.split()))
				if len(cross) > 10:
					return
				cross.pop(0)
				for char in cross:
					c.privmsg(self.channel,char)
			if re.match(u'[\u4e00-\u9faf]',m) or re.match(u'[\u3040-\u309f]',m) or re.match(u'[\u30a0-\u30ff]',m):
				c.privmsg(self.channel,'ching chong bing bong arigatoe gozaymos :33333')
		return

def main():
	import sys
	if len(sys.argv) != 4:
		print("Usage: testbot <server[:port]> <channel> <nickname>")
		sys.exit(1)

	s = sys.argv[1].split(":", 1)
	server = s[0]
	if len(s) == 2:
		try:
			port = int(s[1])
		except ValueError:
			print("Error: Erroneous port.")
			sys.exit(1)
	else:
		port = 6667
	channel = sys.argv[2]
	nickname = sys.argv[3]

	bot = fuukochan(channel, nickname, server, port)
	bot.start()

if __name__ == "__main__":
	main()
