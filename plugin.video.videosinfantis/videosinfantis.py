#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,sys,xbmcaddon
import socket
from urllib2 import urlopen, URLError, HTTPError
socket.setdefaulttimeout( 23 )  # timeout in seconds

addon_id = 'plugin.video.videosinfantis'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'

################################################## 
#MENUS

def CATEGORIESvi(siteurl):
	try :
		req = urllib2.Request(siteurl)
		req.add_header('User-Agent', user_agent)
		response = urllib2.urlopen(req)	
	except HTTPError, e:
		addDir(str(e.code),siteurl,1,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',False)
		print 'The server couldn\'t fulfill the request. Reason:', str(e.code)
	except URLError, e:
		addDir(str(e.reason),siteurl,1,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',False)
		print 'We failed to reach a server. Reason:', str(e.reason)
	else :
		addDir('[COLOR yellow]Inicio[/COLOR]','','','http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True)	
		addDir('Pesquisar',siteurl,3,addonfolder+artfolder+'iconVI.png',True)
		addDir('Últimos',siteurl,1,addonfolder+artfolder+'iconVI.png',True)
		addDir('Filmes',siteurl+'/category/filmes-2/',1,addonfolder+artfolder+'iconVI.png',True)
		addDir('História',siteurl+'/category/historia-2/',1,addonfolder+artfolder+'iconVI.png',True)
		addDir('Música',siteurl+'/category/musica/',1,addonfolder+artfolder+'iconVI.png',True)
		addDir('Séries',siteurl+'/category/series/',1,addonfolder+artfolder+'iconVI.png',True)
		addDir('[A-D]',siteurl+'/category/a-d/',1,addonfolder+artfolder+'iconVI.png',True)
		addDir('[E-H]',siteurl+'/category/e-h/',1,addonfolder+artfolder+'iconVI.png',True)	
		addDir('[I-L]',siteurl+'/category/i-l/',1,addonfolder+artfolder+'iconVI.png',True)
		addDir('[M-P]',siteurl+'/category/m-p/',1,addonfolder+artfolder+'iconVI.png',True)
		addDir('[Q-T]',siteurl+'/category/q-t/',1,addonfolder+artfolder+'iconVI.png',True)	
		addDir('[U-Z]',siteurl+'/category/u-z/',1,addonfolder+artfolder+'iconVI.png',True)	
		
##################################################
#FUNCOES

def pesquisa(siteurl):
      keyb = xbmc.Keyboard('', 'Videos Infantis')
      keyb.doModal()
      if (keyb.isConfirmed()):
            search = keyb.getText()
            if search=='': sys.exit(0)
            encode=urllib.quote(search)
            urlfinal=siteurl+'?s=' + encode + '&x=0&y=0'
            listar_videos(urlfinal,siteurl)
			
def listar_videos(url,siteurl):
	codigo_fonte = abrir_url(url)	
	addDir('[COLOR yellow]Inicio[/COLOR]',siteurl,4,'',True)			
	match = re.compile('<img src="(.+?)"  class="linkimage" alt="(.+?)" title=".+?" />\s+<div class="overlay"> </div>\s+<div class="post-info2">\s+<center>\s+</br>\s+<a href="(.+?)" title=".+?"><img src=".+?" style="margin: 0px 0px 0px 0px; border: none;" alt="Ver video Agora" /></a>').findall(codigo_fonte)
	for img,titulo,url in match:
		titulo = subststring(titulo)
		titulo,url = encontrar_tipo_da_fonte(url,titulo)
		if titulo <> '-': addDir(titulo,url,2,img,False)
	match = re.compile('<img src="(.+?)"  class="linkimage" alt="(.+?)" title=".+?" />\s+<div class="overlay"> </div>\s+<div class="post-info2">\s+<center>\s+<a href="(.+?)" title=".+?"><img src=".+?" style="margin: 0px 0px 0px 0px; border: none;" alt="Ver video Agora" /></a>').findall(codigo_fonte)
	for img,titulo,url in match:
		titulo = subststring(titulo)
		titulo,url = encontrar_tipo_da_fonte(url,titulo)
		if titulo <> '-': addDir(titulo,url,2,img,False)
	match = re.compile('href="(.+?)" >&laquo; Previous Entries</a>').findall(codigo_fonte)	
	if match:
		nexturl = match[0]
		addDir('[COLOR yellow]Proximo >>[/COLOR]',nexturl,1,'',True)
		addDir('[COLOR yellow]Inicio[/COLOR]',siteurl,4,addonfolder+artfolder+'iconVI.png',True)				

def encontrar_tipo_da_fonte(url,titulo):
	codigo_fonte = abrir_url(url)
	match = re.compile('id_video=(.+?)"').findall(codigo_fonte)	
	if match:
		urldaily = getStreamUrlVL(match[0])
		return titulo + ' [COLOR green](Fonte: videolog.tv)[/COLOR]',urldaily
	match = re.compile('file=(.+?)/mov/.+?"').findall(codigo_fonte)
	if match: return titulo + ' [COLOR green](Fonte: sapo.pt)[/COLOR]',match[0]+'/mov'
	#match = re.compile('').findall(codigo_fonte)
	match = re.compile('<div id="video-inside"> (.+?) </div>').findall(codigo_fonte)	
	if match:
		if match[0].find('youtube') > -1:
			match2 = re.compile('youtube.com/embed/(.+?)["\\?]').findall(match[0])
			if not match2:
				match2 = re.compile('youtube.com/embed/(.+?)').findall(match[0])
			if match2:
				urlfound,source = url_solver('http://youtube.com/embed/'+match2[0])
				if urlfound <> '-': return titulo +' [COLOR green](Fonte: '+source+')[/COLOR]',urlfound
		elif match[0].find('vimeo') > -1:
			match2 = re.compile('player.vimeo.com/video/(.+?)["\\?]').findall(match[0])
			if match2:
				urlfound,source = url_solver('http://vimeo.com/'+match2[0])
				if urlfound <> '-': return titulo +' [COLOR green](Fonte: '+source+')[/COLOR]',urlfound
		elif match[0].find('dailymotion') > -1:
			match2 = re.compile('www.dailymotion.com/embed/video/(.+?)["\\?]').findall(match[0])
			if match2:
				urlfound,source = url_solver('http://www.dailymotion.com/video/'+match2[0])
				if urlfound <> '-': return titulo +' [COLOR green](Fonte: '+source+')[/COLOR]',urlfound
		elif match[0].find('zapkolik') > -1:
			codigo_fonte2 = abrir_url(match[0])
			match2 = re.compile('vid.src = \'(.+?)\'').findall(codigo_fonte2)
			if match2: return titulo + ' [COLOR green](Fonte: zapkolik.com)[/COLOR]',match2[0]
		elif match[0].find('mais.uol.com.br') > -1:
			return '-','-'
			#match2 = re.compile('<a href="(.+?)">').findall(match[0])	
			#if match2:
			#	codigo_fonte2 = abrir_url(match2[0])
			#	match2 = re.compile('<input type="hidden" id="postMediaFilePath" value="http://storage.mais.uol.com.br/(.+?).flv" />').findall(codigo_fonte2)
			#	if match2:
			#		videolink = 'http://video21.mais.uol.com.br/'+match2[0]+'.mp4%3Fver%3D1&r%3Dhttp%3A%2F%2Fplayer.mais.uol.com.br%2Fplayer_video_v2.swf'
			#		return titulo + ' [COLOR green](Fonte: mais.uol.com.br)[/COLOR]',videolink			
		else:
			urlfound,source = url_solver('http:'+match[0])
			if urlfound <> '-': return titulo +' [COLOR green](Fonte: '+source+')[/COLOR]',urlfound
	return titulo + ' [COLOR red](Fonte Não Suportada)[/COLOR]','http://google.pt'

def url_solver(urlfinal):
	import urlresolver
	sources=[]
	hosted_media = urlresolver.HostedMediaFile(url=urlfinal)
	sources.append(hosted_media)
	source = urlresolver.choose_source(sources)
	if source: 
		stream_url = source.resolve()
		stream_source = source.get_host()
	else: 
		stream_url = '-'
		stream_source = '-'
	return stream_url,stream_source

def getStreamUrlVL(id):
	content = abrir_url("http://videolog.tv/"+id)
	match = re.compile('<meta property="og:image" content="http://videos.videolog.tv/(.+?)/(.+?)/'+id).findall(content)
	for first,last in match: return 'http://videos.videolog.tv/'+first+'/'+last+'/'+id+'_HD.mp4'		
		
def subststring(titulo):
	titulo = titulo.replace('&#8211;','-')	
	titulo = titulo.replace('&#038;','e')
	return titulo
			
#####################################################
#FUNCOES JÁ FEITAS

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
		
def addDir(name,url,mode,iconimage,pasta):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',addonfolder+artfolder+'videosinfantis.jpg')			
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta)
        return ok

##############################
#GET PARAMS

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

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
