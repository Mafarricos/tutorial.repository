# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import urllib,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
from lib import util
from lib import basic
from HTMLParser import HTMLParser

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
dataPath            = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile")).decode("utf-8")
cachePath			= os.path.join(dataPath,'cache')
sitesfile 			= os.path.join(os.path.join(addonPath, 'resources'),'sites.txt')
site9gagfile 		= os.path.join(cachePath,'_9gag.txt')
sitecachefile 		= os.path.join(cachePath,'_cache.txt')

if not os.path.exists(dataPath): os.makedirs(dataPath)
if not os.path.exists(cachePath): os.makedirs(cachePath)

def MAIN():
	addDir('[COLOR yellow]Listar Videos[/COLOR]','videos',6,'',True,2,'','','')
	addDir('[COLOR grey]Gerir Sites[/COLOR]','next',3,'',True,2,'','',index)

def videosmenu(index=None):
	parser = HTMLParser()
	linecache = ''
	if index == None:
		index = 0		
		open(site9gagfile, 'w').close()
		open(sitecachefile, 'w').close()
	else: index = int(index) + 1
	unique_stuff = util.getpages(index,sitesfile,site9gagfile,cachePath)
	total = len(unique_stuff)
	linecache= basic.readalllines(sitecachefile)	
	for link in unique_stuff:
		if link['url'] not in str(linecache):
			basic.writefile(sitecachefile,"a",'::pageindex::'+str(index)+'::'+link['url']+'::\n')
			informacao = { "Title": parser.unescape(link['title'])}	
			addDir(parser.unescape(link['title'])+' [COLOR yellow]['+link['prettyname']+'][/COLOR]',link['url'],1,link['thumbnail'],False,total,link['duration'],informacao,index)
		elif '::pageindex::'+str(index)+'::'+link['url'] in str(linecache):
			informacao = { "Title": parser.unescape(link['title'])}			
			addDir(parser.unescape(link['title'])+' [COLOR yellow]['+link['prettyname']+'][/COLOR]',link['url'],1,link['thumbnail'],False,total,link['duration'],informacao,index)		
	addDir('Seguinte >>','next',6,'',True,1,'','',index)

	
def listingsites():
	list = basic.listsites(sitesfile)
	total = len(list)
	addDir('[COLOR yellow]Todos (On)[/COLOR]','on',4,'',False,total,'','',0)
	addDir('[COLOR yellow]Todos (Off)[/COLOR]','off',4,'',False,total,'','',0)
	addDir('[COLOR red]Remover Cache[/COLOR]','cache',5,'',False,total,'','',0)	
	for sites in list:
		if 'true' in sites['enabled']: addDir('[COLOR green](On)[/COLOR]  '+sites['url'],sites['url'],4,'',False,total,'','',0)
		if 'false' in sites['enabled']: addDir('[COLOR red](Off)[/COLOR] '+sites['url'],sites['url'],4,'',False,total,'','',0)

def changestatus(url):
	import fileinput,sys
	for line in fileinput.input(sitesfile, inplace = 1):
		if url=='on': line = line.replace('"enabled":"false"','"enabled":"true"')
		elif url=='off': line = line.replace('"enabled":"true"','"enabled":"false"')		
		elif url in line: 
			if '"enabled":"true"' in line: line = line.replace('"enabled":"true"','"enabled":"false"')
			elif '"enabled":"false"' in line: line = line.replace('"enabled":"false"','"enabled":"true"')
		sys.stdout.write(line)
	xbmc.executebuiltin("Container.Refresh")
	
def play(url):
	playlist = xbmc.PlayList(1)
	playlist.clear()             
	playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=str(iconimage))) 
	try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	except: pass

def addDir(name,url,mode,iconimage,pasta,total,duration,informacao,index):
	context = []
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('ascii', 'xmlcharrefreplace'))+"&index="+str(index)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',addonPath+'/fanart.jpg')
	if informacao <> '': liz.setInfo( type="Video", infoLabels=informacao )	
	if duration <> '': liz.addStreamInfo('Video', {"duration":duration})
	context.append(('E-Mail', 'RunPlugin(%s?mode=7&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),name)))
	liz.addContextMenuItems(context, replaceItems=False)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
        return param
      
params=get_params()
url=None
name=None
mode=None
iconimage=None
index=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: index=urllib.unquote_plus(params["index"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)
print "Index: "+str(index)

if mode==None or url==None or len(url)<1: MAIN()
elif mode==1: play(url)
elif mode==2: MAIN()
elif mode==3: listingsites()
elif mode==4: changestatus(url)
elif mode==5: xbmcgui.Dialog().ok('Cache',basic.removecache(cachePath))
elif mode==6: videosmenu(index)
elif mode==7: util.send_email(name,url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))