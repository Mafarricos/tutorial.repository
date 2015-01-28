#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,sys
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

def CATEGORIESgato(siteurl):
	try :
		req = urllib2.Request(siteurl)
		req.add_header('User-Agent', user_agent)
		response = urllib2.urlopen(req)	
		#response = urlopen( siteurl )
	except HTTPError, e:
		addDir(str(e.code),siteurl,1,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',False)
		print 'The server couldn\'t fulfill the request. Reason:', str(e.code)
	except URLError, e:
		addDir(str(e.reason),siteurl,1,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',False)
		print 'We failed to reach a server. Reason:', str(e.reason)
	else :
		addDir('[COLOR yellow]Inicio[/COLOR]','','','http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True)		
		addDir('Top',siteurl,6,addonfolder+artfolder+'icongato.png',True)
		addDir('Desenhos Animados (Anos 70)',siteurl+'/category/desenhos-animados/anos-70/',7,addonfolder+artfolder+'icongato.png',True)		
		addDir('Desenhos Animados (Anos 80)',siteurl+'/category/desenhos-animados/anos-80/',7,addonfolder+artfolder+'icongato.png',True)		
		addDir('Desenhos Animados (Anos 90)',siteurl+'/category/desenhos-animados/anos-90/',7,addonfolder+artfolder+'icongato.png',True)		
		addDir('Música',siteurl+'category/musicas/',7,addonfolder+artfolder+'icongato.png',True)
		addDir('Cinema',siteurl+'category/cinema/',7,addonfolder+artfolder+'icongato.png',True)	
		addDir('Programas TV',siteurl+'category/programas-tv/',7,addonfolder+artfolder+'icongato.png',True)	
		
##################################################
#FUNCOES
			
def listar_videos(url):
	codigo_fonte = abrir_url(url)	
	addDir('[COLOR yellow]Inicio[/COLOR]',url,5,addonfolder+artfolder+'icongato.png',True)			
	print codigo_fonte
	match = re.compile('" href="(.+?)" title=".+?"><img src=".+?" width="\d+" height="\d+" alt="" /> </a>\s+</figure>\s+</div>\s+<h1 class="title">(.+?)</h1>\s+<p></p>\s+<footer class="aligncenter">\s+<a href="(.+?)" class="button medium button-style1">Ver</a>').findall(codigo_fonte)
	for img,titulo,url in match:
		titulo = subststring(titulo)	
		addDir(titulo,url,2,img,False)

def listar_videos_category(url):
	codigo_fonte = abrir_url(url)	
	addDir('[COLOR yellow]Inicio[/COLOR]',url,5,addonfolder+artfolder+'icongato.png',True)			
	print codigo_fonte
	match = re.compile('<h1><a href="(.+?)">(.+?)</a></h1>\s+</div><!--/ post-title-->\s+<div class="border-shadow alignleft">\s+<figure>\s+<a class="prettyPhoto" title=".+?" href="(.+?)">').findall(codigo_fonte)
	for url,titulo,img in match:
		titulo = subststring(titulo)
		addDir(titulo,url,2,img,False)
	match = re.compile('<link rel="next" href="(.+?)" />').findall(codigo_fonte)	
	if match:
		nexturl = match[0]
		addDir('[COLOR yellow]Proximo >>[/COLOR]',nexturl,7,'',True)
		addDir('[COLOR yellow]Inicio[/COLOR]',url,5,addonfolder+artfolder+'icongato.png',True)				

def encontrar_tipo_da_fonte(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('youtube.com/embed/(.+?)"').findall(codigo_fonte)
	if match:
		return 'plugin://plugin.video.youtube/?action=play_video&videoid='+match[0]
	return 'NOTSUPPORT'
		
def subststring(titulo):
	titulo = titulo.replace('&#8211;', '-')	
	titulo = titulo.replace('&#038;', 'e')
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
	liz.setProperty('fanart_image',addonfolder+artfolder+'ogatodasbotas.jpg')		
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
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]                            
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