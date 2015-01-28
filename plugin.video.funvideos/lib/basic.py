# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import os,json
from HTMLParser import HTMLParser

def cleanTitle(title):
	title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", "\"").replace("&ndash;", "-").replace('\\','')
	title = title.replace('"',"")
	title = title.strip()
	return title

def open_url(url,type=None):
	if type=='9gag':
		try:
			import requests
			page = requests.get(url)
			return page.text
		except BaseException as e: print '##ERROR-funvideos:open_url: '+str(url)+' '+str(e)		
	else:
		try:
			import urllib2
			user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
			req = urllib2.Request(url)
			req.add_header('User-Agent', user_agent)
			response = urllib2.urlopen(req)
			link=response.read()
			response.close()
			return link
		except BaseException as e: print '##ERROR-funvideos:open_url: '+str(url)+' '+str(e)	
	
def listsites(sitesfile):
	list = []
	ins = open(sitesfile, "r" )	
	for line in ins: 
		parameters = json.loads(line)
		url=parameters['site']
		enabled=parameters['enabled']		
		list.append(json.loads('{"url":"'+url+'","enabled":"'+enabled+'"}'))						
	return list

def readoneline(file):
	f = open(file,"r")
	line = f.read()
	f.close()
	return line

def readalllines(file):
	f = open(file,"r")
	lines = f.readlines()
	f.close()
	return lines

def readfiletoJSON(file):
	f = open(file,"r")
	line = f.read().strip('\n')
	f.close()	
	return line
	
def writefile(file,mode,string):
	writes = open(file, mode)
	writes.write(string)
	writes.close()

def removecache(cachePath):
	try:
		for root,dir,files in os.walk(cachePath):
			for f in files:
				if not '_cache' in f and not '_9gag' in f: os.unlink(os.path.join(root, f))
		return 'Eliminação Completa.'
	except BaseException as e: return str(e)