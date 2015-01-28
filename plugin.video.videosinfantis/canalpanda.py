#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2013 enen92 
#	adapted by Mafarricos
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

import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,xbmcvfs,socket

addon_id = 'plugin.video.videosinfantis'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'

def CATEGORIESpanda(base_url):
        addDir('[COLOR yellow][B]Inicio[/B][/COLOR]','','','')
        addDir('[COLOR orange][B]MAIS VOTADOS[/B][/COLOR]',base_url+'panda-tv/PVideoListagem?filterorder=1&pageNumber=1',8, addonfolder + artfolder + 'maisvotados.png')
        addDir('[COLOR orange][B]MAIS RECENTES[/B][/COLOR]',base_url+'panda-tv/PVideoListagem?filterorder=2&pageNumber=1',8, addonfolder + artfolder + 'maisrecentes.png')
        addDir('[COLOR orange][B]MAIS VISTOS[/B][/COLOR]',base_url+'panda-tv/PVideoListagem?filterorder=3&pageNumber=1',8, addonfolder + artfolder + 'maisvistos.png')
        addDir('[COLOR orange][B]POR SÉRIES[/B][/COLOR]',base_url+'panda-tv/PVideoListagem?filterorder=4&pageNumber=1',8, addonfolder + artfolder + 'porseries.png')
        addDir('[COLOR orange][B]PESQUISAR[/B][/COLOR]',base_url,9, addonfolder + artfolder + 'pesquisar.png')
	#xbmc.executebuiltin("Container.SetViewMode(500)")


def programa_paginicial(url,page_logical,base_url):
	if page_logical == '0':
		pag_num = '1'
		filtervalue=re.compile('filtervalue=(.+?)&').findall(url) #verifica se é um parametro de pesquisa
		filterorder=re.compile('filterorder=(.+?)&').findall(url) #Indica como a listagem é feita
		if filtervalue == []: # Se não for uma pesquisa
			url=base_url+'panda-tv/PVideoListagem?filterorder=' + filterorder[0] + '&pageNumber=' + pag_num
		else:
			url=base_url+'panda-tv/PVideoListagem?filtervalue=' + filtervalue[0] + '&pageNumber=' + pag_num
		addDir('[B][COLOR red]Ver Todos[/B][/COLOR]',url,10,addonfolder + artfolder + 'playlist.png')
		link = abrir_url(url)
		thumbarray=re.compile('src="(.+?).jpg"').findall(link)
		print thumbarray
		print 'o primeiro é' + thumbarray[0]	
		counter = 0
		match=re.compile('changeVideoToDisplay\(\'(.+?)\'').findall(link)
		pag_num_total=re.compile('pagInfoTop">.+?de (.+?)</div>').findall(link)
 		for urltmp in match:
			urltmp=urltmp.replace('ó', "%C3%B3")
			thumbtmp = thumbarray[int(counter)]
			link2 = abrir_url(base_url + urltmp)
			titulo=re.compile('<h3>(.+?)</h3>').findall(link2)
			urlvideo=re.compile('<a href="(.+?).mp4"').findall(link2)
			urlvideo=urlvideo[0].replace(' ', "%20");
			plotarray1=re.compile('<p>(.+?)\n(.+?)</p>').findall(link2)
			plotarray2=re.compile('<p>(.+?)</p>').findall(link2)
			plotarray3=re.compile('<p>(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)</p>').findall(link2)
			plotarray4=re.compile('<p>(.+?)\n(.+?)\n(.+?)\n(.+?)</p>').findall(link2)
			plotarray5=re.compile('<p>(.+?)\n(.+?)\n(.+?)</p>').findall(link2)
			if plotarray1 == []:
				if plotarray2 == []:
					if plotarray3 == []:
						if plotarray4 == []:	
							if plotarray5 == []:
								plot = 'Informação não disponivel'
							else:
								plot = plotarray5[0][0] + ' ' + plotarray5[0][1] + ' ' + plotarray5[0][2]
						else:
							plot = plotarray4[0][0] + ' ' + plotarray4[0][1] + ' ' + plotarray4[0][2] + ' ' + plotarray4[0][3] 
					else:
						plot = plotarray3[0][0] + ' ' + plotarray3[0][1] + ' ' + plotarray3[0][2] + ' ' + plotarray3[0][3] + ' ' + plotarray3[0][4]
				else:
					plot = plotarray2[0]
			else:
				plot = plotarray1[0][0] + ' ' + plotarray1[0][1]					
			
			print plot
			thumbnail=base_url + thumbtmp + '.jpg'
			addLink_panda('[B][COLOR orange]' + titulo[0] + '[/COLOR][/B]',base_url + urlvideo + '.mp4',thumbnail,plot)
			counter += 1
		if pag_num_total == []:
			print 'nao tem nada'
			pass
		else:
			existepagseguinte=re.compile('pagNext.+?/panda-tv/(.+?)=').findall(link)
			if existepagseguinte == []:
				pass
			else:
				if filtervalue == []: # Se não for uma pesquisa
					print 'filterorder', filterorder[0]
					botaoseguinte(pag_num,pag_num_total[0],filterorder[0],'')
				else:
					botaoseguinte(pag_num,pag_num_total[0],'',filtervalue[0])
		#xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		#xbmc.executebuiltin("Container.SetViewMode(515)")
	else:
		filtervalue=re.compile('filtervalue=(.+?)&').findall(url) #verifica se é um parametro de pesquisa
		print 'o url e ' + url	
		filterorder=re.compile('filterorder=(.+?)&').findall(url) #Indica como a listagem é feita
		print 'filterorder detectado', filterorder
		pag_num=re.compile('pageNumber=(\d+)').findall(url)
		print pag_num
		link = abrir_url(url)
		thumbarray=re.compile('src="(.+?).jpg"').findall(link)
		print thumbarray
		print 'o primeiro é' + thumbarray[0]	
		counter = 0
		match=re.compile('changeVideoToDisplay\(\'(.+?)\'').findall(link)
		pag_num_total=re.compile('pagInfoTop">.+?de (.+?)</div>').findall(link)
		print pag_num_total[0]
 		for urltmp in match:
			urltmp=urltmp.replace('ó', "%C3%B3")
			thumbtmp = thumbarray[int(counter)]
			print 'encontrei url', base_url + urltmp
			link2 = abrir_url(base_url + urltmp)
			titulo=re.compile('<h3>(.+?)</h3>').findall(link2)
			urlvideo=re.compile('<a href="(.+?).mp4"').findall(link2)
			urlvideo=urlvideo[0].replace(' ', "%20");
			plotarray1=re.compile('<p>(.+?)\n(.+?)</p>').findall(link2)
			plotarray2=re.compile('<p>(.+?)</p>').findall(link2)
			plotarray3=re.compile('<p>(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)</p>').findall(link2)
			plotarray4=re.compile('<p>(.+?)\n(.+?)\n(.+?)\n(.+?)</p>').findall(link2)
			plotarray5=re.compile('<p>(.+?)\n(.+?)\n(.+?)</p>').findall(link2)
			if plotarray1 == []:
				if plotarray2 == []:
					if plotarray3 == []:
						if plotarray4 == []:	
							if plotarray5 == []:
								plot = 'Informação não disponivel'
							else:
								plot = plotarray5[0][0] + ' ' + plotarray5[0][1] + ' ' + plotarray5[0][2]
						else:
							plot = plotarray4[0][0] + ' ' + plotarray4[0][1] + ' ' + plotarray4[0][2] + ' ' + plotarray4[0][3] 
					else:
						plot = plotarray3[0][0] + ' ' + plotarray3[0][1] + ' ' + plotarray3[0][2] + ' ' + plotarray3[0][3] + ' ' + plotarray3[0][4]
				else:
					plot = plotarray2[0]
			else:
				plot = plotarray1[0][0] + ' ' + plotarray1[0][1]					
			
			print plot
			thumbnail=base_url + thumbtmp + '.jpg'
			addLink_panda('[B][COLOR orange]' + titulo[0] + '[/COLOR][/B]',base_url + urlvideo + '.mp4',thumbnail,plot)
			counter += 1
		if pag_num_total == []:
			print 'nao tem nada'
			pass
		else:
			existepagseguinte=re.compile('pagNext.+?/panda-tv/(.+?)=').findall(link)
			if existepagseguinte == []:
				pass
			else:
				if filtervalue == []: # Se não for uma pesquisa
					print 'filterorder', filterorder[0]
					botaoseguinte(pag_num[0],pag_num_total[0],filterorder[0],'')
				else:
					botaoseguinte(pag_num[0],pag_num_total[0],'',filtervalue[0])
		
		#xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		#xbmc.executebuiltin("Container.SetViewMode(515)")

def botaoseguinte(page_num,pag_num_total,filterorder,filtervalue):
	page_next =  int(page_num) + 1
	if filtervalue == '':
		url='http://canalpanda.pt/panda-tv/PVideoListagem?filterorder=' + filterorder + '&pageNumber=' + str(page_next)
	else:
		url='http://canalpanda.pt/panda-tv/PVideoListagem?filtervalue=' + filtervalue + '&pageNumber=' + str(page_next)
	addDir('[B]Pag '+ page_num + '/' + pag_num_total + '[/B][B][COLOR blue] | Seguinte >>[/B][/COLOR]',url,11,addonfolder + artfolder + 'next.png')

def pesquisa(base_url):
	keyb = xbmc.Keyboard('', 'Pesquisa aqui:')
	keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
		pesquisa_resultados(encode,base_url)                

def pesquisa_resultados(encode,base_url):
	url = base_url + '/panda-tv/PVideoListagem?filtervalue=' + encode + '&pageNumber=1'
	link3 = abrir_url(url)
	print link3.find('Não foram encontrados resultados')
	if link3.find('Não foram encontrados resultados') == -1 :
		programa_paginicial(url,'0',base_url)
	else:
		ok = ok_dialog_box('CanalPanda.pt','[B][COLOR red]Não foram encontrados resultados[/COLOR][/B]')

def lista_de_videos(url,filterorder,filtervalue,base_url):
	socket.setdefaulttimeout(1000)
	playlist = xbmc.PlayList(1)
	playlist.clear()	
	progress = xbmcgui.DialogProgress()
	progress.create('CanalPanda.pt', 'O Panda está a obter os vídeos...')
	link = abrir_url(url)
	pag_num=re.compile('pageNumber=(\d+)').findall(url)
	pag_num_total=re.compile('pagInfoTop">.+?de (.+?)</div>').findall(link)
	pag_num_total=int(pag_num_total[0])
	print 'pagnumtotal',pag_num_total
	i = 1
	while i <= pag_num_total:
		if filtervalue == '':
			url = base_url+'panda-tv/PVideoListagem?filterorder=' + filterorder + '&pageNumber=' + str(i)
		else:
			url = base_url+'panda-tv/PVideoListagem?filtervalue=' + filtervalue + '&pageNumber=' + str(i)
		print 'ola'
		link = abrir_url(url)
		thumbarray=re.compile('src="(.+?).jpg"').findall(link)
		counter = 0
		match=re.compile('changeVideoToDisplay\(\'(.+?)\'').findall(link)
		for urltmp in match:
			urltmp=urltmp.replace('ó', "%C3%B3")
			thumbtmp = thumbarray[int(counter)]
			print 'encontrei url', base_url + urltmp
			link2 = abrir_url(base_url + urltmp)
			titulo=re.compile('<h3>(.+?)</h3>').findall(link2)
			urlvideo=re.compile('<a href="(.+?).mp4"').findall(link2)
			urlvideo=urlvideo[0].replace(' ', "%20");
			thumbnail=base_url + thumbtmp + '.jpg'
			listitem = xbmcgui.ListItem('[B][COLOR orange]' + titulo[0] + '[/COLOR][/B]', iconImage="DefaultVideo.png", thumbnailImage=thumbnail) 
			playlist.add(base_url + urlvideo + '.mp4', listitem)
			counter += 1

		percent = int( ( i / float(pag_num_total) ) * 100)
		print 'percent',percent
    		message = "Página " + str(i) + " de " + str(pag_num_total)
    		progress.update( percent, "", message, "" )
    		print "Página " + str(i) + " de " + str(pag_num_total)
    		xbmc.sleep( 1000 )
    		if progress.iscanceled():
        		break
    		i = i + 1
		print i
	progress.close()
	addDir('[B][COLOR orange]Volta atrás[/COLOR][/B]',base_url,12,'')
	player = Player()
	player.play(playlist)
	while player._playbackLock:
		player._trackPosition()
		xbmc.sleep(250)

############################################################################################################################

ok_dialog_box = xbmcgui.Dialog().ok

#Retirado do ADDON do j0anita!
class Player(xbmc.Player):
      def __init__(self):
            xbmc.Player.__init__(self, xbmc.PLAYER_CORE_AUTO)
            self._playbackLock = True
            self._totalTime = 999999
            self._lastPos = 0
            print "Criou o player"

      def onPlayBackStarted(self):
            print "Comecou o player"
            self._totalTime = self.getTotalTime()

      def onPlayBackStopped(self):
            print "Parou o player"
            self._playbackLock = False
            playedTime = int(self._lastPos)
            watched_values = [.7, .8, .9, .95]
            min_watched_percent = watched_values[int(selfAddon.getSetting('watched-percent'))]
            print 'playedTime / totalTime : %s / %s = %s' % (playedTime, self._totalTime, playedTime/self._totalTime)
            if playedTime == 0 and self._totalTime == 999999: raise PlaybackFailed('XBMC falhou a comecar o playback')
            else:
                  print ''

      def onPlayBackEnded(self):              
            self.onPlayBackStopped()
            print 'Chegou ao fim. Playback terminou.'

      def _trackPosition(self):
            try: self._lastPos = self.getTime()
            except: print 'Erro quando estava a tentar definir o tempo de playback'

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

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

def addLink_panda(name,url,iconimage,plot):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', 'http://canalpanda.pt/Images/fundoPandaTV.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', 'http://canalpanda.pt/Images/fundoPandaTV.jpg')
        liz.setInfo( type="Video", infoLabels={ "Title": name })
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

params=get_params()
url=None
name=None
mode=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass