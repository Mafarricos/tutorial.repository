#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# Thanks to enen92 and fightnight
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon
import videosinfantis
import ogatodasbotas
import canalpanda
import kidsyoutube

addon_id = 'plugin.video.videosinfantis'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'
siteurl = 'http://videosinfantis.pt/'
siteurl2 = 'http://videos.ogatodasbotas.com/'
siteurl3 = 'http://canalpanda.pt/'

################################################## 
#MENUS

def CATEGORIES():
	kidsyoutube.addDir('Kids Youtube',siteurl,13,addonfolder+artfolder+'iconKyou.png',True,1,'',maxresults,startindex,'')
	videosinfantis.addDir('Videos Infantis',siteurl,4,addonfolder+artfolder+'iconVI.png',True)
	ogatodasbotas.addDir('O Gato das Botas',siteurl2,5,addonfolder+artfolder+'icongato.png',True)	
	canalpanda.addDir('CanalPanda.pt',siteurl3,12,addonfolder+artfolder+'iconpanda.png')
		
##################################################
#FUNCOES

def play(url,name):
  if 'gatodasbotas' in url: url=ogatodasbotas.encontrar_tipo_da_fonte(url)
  listitem = xbmcgui.ListItem()
  listitem.setPath(url)
  listitem.setInfo("Video", {"Title":name})
  listitem.setProperty('IsPlayable', 'true')
  try:
	xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	xbmcPlayer.play(url)
  except:
   pass
   self.message("Couldn't play item.")
   
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

print "#Mode: "+str(mode)
print "#URL: "+str(url)
print "#Name: "+str(name)
print "#Iconimage: "+str(iconimage)
print "#MaxResults: "+str(maxresults)
print "#StartIndex: "+str(startindex)

      
#################################
#MODOS

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: videosinfantis.listar_videos(url,siteurl)
elif mode==2: play(url,name)
elif mode==3: videosinfantis.pesquisa(siteurl)
elif mode==4: videosinfantis.CATEGORIESvi(siteurl)
elif mode==5: ogatodasbotas.CATEGORIESgato(siteurl2)
elif mode==6: ogatodasbotas.listar_videos(url)
elif mode==7: ogatodasbotas.listar_videos_category(url)
elif mode==8: canalpanda.programa_paginicial(url,'0',siteurl3)
elif mode==9: canalpanda.pesquisa(siteurl3)
elif mode==10:
	filterorder=re.compile('filterorder=(.+?)&').findall(url)
	filtervalue=re.compile('filtervalue=(.+?)&').findall(url)
	if filterorder==[]: canalpanda.lista_de_videos(url,'',filtervalue[0],siteurl3)
	else: canalpanda.lista_de_videos(url,filterorder[0],'',siteurl3)
elif mode==11: canalpanda.programa_paginicial(url,'1',siteurl3)
elif mode==12: canalpanda.CATEGORIESpanda(siteurl3)
elif mode==13: kidsyoutube.CATEGORIESyou()
elif mode==14: kidsyoutube.listchannel(name,url,maxresults,startindex)
elif mode==15: kidsyoutube.playlistchannel(name,url,maxresults,startindex)
elif mode==16: kidsyoutube.MenuCreate(name,url,maxresults,startindex)
elif mode==17: kidsyoutube.playlistListing(name,url,maxresults,startindex)
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))