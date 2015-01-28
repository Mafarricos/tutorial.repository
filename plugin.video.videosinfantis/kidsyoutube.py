#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,sys,xbmcaddon,math
import socket
from urllib2 import urlopen, URLError, HTTPError
socket.setdefaulttimeout( 23 )  # timeout in seconds

addon_id = 'plugin.video.videosinfantis'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
#channels = ["BabyTVPortugues","TuTiTuTV","PandaEOsCaricasVEVO","XanaTocToc","juptube","PocoyoBrazil","jato6661","disneyportugal","Tugaanimado","PTDisney","LisseDisneyPT","dunuca","UCV-By_7ySjgss2k5SVFMPjg"]

###################################################MENUS

def CATEGORIESyou():
		content = abrir_url("http://addons-xbmc-mafarricos.googlecode.com/svn/kidsyoutube/canal.txt")	
		channels = re.findall(':Canal:(.+?):End:',content,re.DOTALL)
		maxresults=15
		startindex=1
		addDir('[COLOR green]KIDS YOUTUBE[/COLOR]','','','http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',False,1,'',maxresults,startindex,'')		
		addDir('[COLOR yellow]Inicio[/COLOR]','','','http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True,1,'',maxresults,startindex,'')
		numero_de_canais = len(channels)	
		for channel in channels:
			content = abrir_url('https://gdata.youtube.com/feeds/api/users/'+channel+'/uploads?v=2.1')
			match = re.compile('<name>(.+?)</name>').findall(content)		
			totalresults = re.compile('<openSearch:totalResults>(\d+)</openSearch:totalResults>').findall(content)				
			addDir(match[0]+' [COLOR blue]('+totalresults[0]+' Videos)[/COLOR]',channel,16,addonfolder+artfolder+'iconKyou.png',True,numero_de_canais,'',maxresults,startindex,'')

def MenuCreate(name,url,maxresults,startindex):
		addDir('[COLOR green]'+name+'[/COLOR]',url,'',addonfolder+artfolder+'iconKyou.png',False,1,'',maxresults,startindex,'')			
		addDir('[COLOR yellow]Inicio[/COLOR]',url,13,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True,1,'',maxresults,startindex,'')	
		addDir('[COLOR yellow]Todos[/COLOR]',url,14,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True,1,'',maxresults,startindex,'')			
		addDir('[COLOR yellow]Playlists[/COLOR]',url,17,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True,1,'',maxresults,startindex,'')					

def playlistListing(name,url,maxresults,startindex):
		content = abrir_url('https://gdata.youtube.com/feeds/api/users/'+url+'/playlists?max-results=50&start-index=1&v=2&orderby=published')
		match = re.compile('<name>(.+?)</name>').findall(content)				
		addDir('[COLOR green]'+match[0]+'[/COLOR]',url,'',addonfolder+artfolder+'iconKyou.png',False,1,'',maxresults,startindex,'')			
		addDir('[COLOR yellow]Inicio[/COLOR]',url,13,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True,1,'',maxresults,startindex,'')	
		entry = re.compile('<entry(.+?)</entry>').findall(content)
		numeroentries = len(entry)			
		if numeroentries == 0: addDir('[COLOR red]SEM PLAYLISTS[/COLOR]',url,'','http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',False,1,'',maxresults,startindex,'')			
		for entries in entry:
			countHit = re.findall('<yt:countHint>(\d+)</yt:countHint>',entries,re.DOTALL)
			name = re.findall('<title>(.+?)</title>',entries,re.DOTALL)
			url = re.findall('<link rel=\'alternate\' type=\'text/html\' href=\'(.+?)\'/>',entries,re.DOTALL)
			img = re.findall('name=\'mqdefault\'/><media:thumbnail url=\'(.+?)\'',entries,re.DOTALL)				
			if countHit[0]<>0: addDir(name[0]+' ('+countHit[0]+' Videos)',url[0],14,img[0],True,numeroentries,'',maxresults,startindex,'')						
			
def listchannel(name,url,maxresults,startindex):	
	addDir('[COLOR yellow]Inicio[/COLOR]',url,13,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True,1,'',maxresults,startindex,'')	
	addDir('[COLOR yellow]Criar Playlist[/COLOR]',url,15,addonfolder+artfolder+'iconKyou.png',False,1,'',maxresults,startindex,'')
	if 'playlist' in url:
#		if maxresults == None: maxresults = 15
#		if startindex == None: startindex = 1
		url3 = url.replace("https://www.youtube.com/playlist?list=","")
		content = abrir_url('https://gdata.youtube.com/feeds/api/playlists/'+url3+'?max-results='+str(maxresults)+'&start-index='+str(startindex)+'&v=2.1')	
	else: content = abrir_url('https://gdata.youtube.com/feeds/api/users/'+url+'/uploads?v=2.1&max-results='+str(maxresults)+'&start-index='+str(startindex))
	content = replacecontent(content)	
#	dateadded = '';
#	genre ='';
#	credits='';
#	plot='';
	#print "##content "+content
	entry = re.compile('<entry(.+?)</entry>').findall(content)	
	totalresults = re.compile('<openSearch:totalResults>(\d+)</openSearch:totalResults>').findall(content)
	numero_de_videos = len(entry)
	totalpages = int(math.ceil(float(totalresults[0])/float(maxresults)))	
	for entries in entry:
		duracao = re.findall('<yt:duration seconds=\'(\d+)\'/>',entries,re.DOTALL)
		if not duracao: duracao[0] = '0'
		titulo = re.findall('<title>(.+?)</title>',entries,re.DOTALL)
		url2 = re.findall('<link rel=\'alternate\' type=\'text/html\' href=\'(.+?)\'/>',entries,re.DOTALL)
		img = re.findall('name=\'mqdefault\'/><media:thumbnail url=\'(.+?)\'',entries,re.DOTALL)	
		if not img: img[0]=''
		plot = re.findall('<media:description type=\'plain\'>(.+?)</media:description>',entries,re.DOTALL)		
		id_video = url2[0].replace("https://www.youtube.com/watch?v=","")
		id_video = id_video.replace("&amp;feature=youtube_gdata","")
		url2='plugin://plugin.video.youtube/?action=play_video&videoid='+id_video
		if not plot: plotresume = ''
		else: plotresume = plot[0].decode("utf-8")
		informacao = { "Title": titulo[0] , "plot": plotresume}
		addDir(titulo[0],url2,2,img[0],False,numero_de_videos,duracao[0],'','',informacao)
	startindex = int(startindex)+int(maxresults)
	pageno = (startindex - 1) / maxresults
	if totalresults:
		if int(totalresults[0]) > int(startindex): addDir('[COLOR yellow]('+str(pageno)+'/'+str(totalpages)+') Próxima >>[/COLOR]',url,14,addonfolder+artfolder+'iconKyou.png',True,1,'',maxresults,startindex,'')
		else: addDir('[COLOR yellow]('+str(pageno)+'/'+str(totalpages)+')[/COLOR]',url,'',addonfolder+artfolder+'iconKyou.png',False,1,'',maxresults,startindex,'')

def replacecontent(content):
	content = content.replace("\n","")
	content = content.replace("\t","")	
	content = content.replace("\r","")	
	return content

def playlistchannel(name,url,maxresults,startindex):
	playlist = xbmc.PlayList(1)
	playlist.clear()	
	progress = xbmcgui.DialogProgress()
	progress.create('Videos Infantis', 'A Criar Playlist!')
	if 'playlist' in url:
		url3 = url.replace("https://www.youtube.com/playlist?list=","")
		content = abrir_url('https://gdata.youtube.com/feeds/api/playlists/'+url3+'?max-results='+str(maxresults)+'&start-index='+str(startindex)+'&v=2.1')	
	else: content = abrir_url('https://gdata.youtube.com/feeds/api/users/'+url+'/uploads?max-results='+str(maxresults)+'&start-index='+str(startindex)+'&v=2.1')	
	content = replacecontent(content)
	match = re.compile('<entry(.+?)</entry>').findall(content)
	totalresults = re.compile('<openSearch:totalResults>(\d+)</openSearch:totalResults>').findall(content)	
	vidsmissing = int(totalresults[0])-int(startindex)+1
	if vidsmissing < maxresults: maxresults = vidsmissing
	i=1
	for entries in match:
		titulo = re.findall('<title>(.+?)</title>',entries,re.DOTALL)
		url2 = re.findall('<link rel=\'alternate\' type=\'text/html\' href=\'(.+?)\'/>',entries,re.DOTALL)
		id_video = url2[0].replace("https://www.youtube.com/watch?v=","")
		id_video = id_video.replace("&amp;feature=youtube_gdata","")
		url2='plugin://plugin.video.youtube/?action=play_video&videoid='+id_video
		listitem = xbmcgui.ListItem('[B][COLOR orange]' + titulo[0].decode("utf-8") + '[/COLOR][/B]', iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png") 
		listitem.setProperty('IsPlayable', 'true')			
		playlist.add(url2, listitem)	
		xbmc.sleep( 100 )
		if progress.iscanceled():
			playlist.clear()
			break
		percent = int( ( i / float(maxresults) ) * 100)
		print 'percent',percent
		message = "Video " + str(i) + " de " + str(maxresults)
		progress.update( percent, "", message, "" )
		i = i + 1
	try:
		progress.close()
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	except:
		pass
		self.message("Couldn't play item.")

def pesquisa(siteurl):
      keyb = xbmc.Keyboard('', 'Videos Infantis')
      keyb.doModal()
      if (keyb.isConfirmed()):
            search = keyb.getText()
            if search=='': sys.exit(0)
            encode=urllib.quote(search)
            urlfinal=siteurl+'?s=' + encode + '&x=0&y=0'
            listar_videos(urlfinal,siteurl)
			
######################################################FUNCOES JÁ FEITAS

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
		
def addDir(name,url,mode,iconimage,pasta,total,duration,maxresults,startindex,informacao):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&maxresults="+str(maxresults)+"&startindex="+str(startindex)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',addonfolder+artfolder+'kidsyoutube.jpg')	
	if duration <> '':
		liz.addStreamInfo('Video', {"duration":duration})
	if informacao <> '':
		liz.setInfo( type="Video", infoLabels=informacao )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
        return ok

###############################GET PARAMS

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
maxresults=None
startindex=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: maxresults=int(params["maxresults"])
except: pass
try: startindex=int(params["startindex"])
except: pass