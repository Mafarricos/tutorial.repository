# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import urllib2,re,threading,os,json,xbmcaddon,xbmcgui,xbmc
from HTMLParser import HTMLParser
import basic,ninegag,Break,vitaminl

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
getSetting          = xbmcaddon.Addon().getSetting

def getpages(id,sitesfile,site9gagfile,cachePath):
	progress = xbmcgui.DialogProgress()
	list = []
	progress.create('Fun Videos', 'A Obter dados...')
	i = 1
	t = 0
	ins = open(sitesfile, "r")	
	for line in ins: t = t + 1
	ins.close()
	ins = open(sitesfile, "r" )	
	for line in ins: 
		percent = int( ( i / float(t) ) * 100)	
		parameters = json.loads(line)
		enabled = parameters['enabled']
		pageindex = parameters['pagination']
		prettyname = parameters['prettyname']
		message = "Site: " + prettyname + " ("+ str(i)+'/'+str(t)+")"		
		progress.update( percent, "", message, "" )
		if progress.iscanceled():
			progress.close()
			xbmcgui.Dialog().ok('ERROR','Cancelled.')
			return ''		
		i = i + 1		
		if 'true' in enabled:
			site = parameters['site']
			frame = parameters['frame']
			starton = int(parameters['starton'])
			print '##funvideos-site: '+site+pageindex+str(id+starton)			
			if 'true' in frame: 
				list2 = grabiframes(site+pageindex+str(id+starton),prettyname,cachePath)
				if list2: list.extend(list2)
			elif 'vit' in frame:
				list2 = vitaminl.grab(site+pageindex+str(id+starton),prettyname,cachePath,getSetting("cachesites"))
				if list2: list.extend(list2)	
			elif '9gag' in frame:
				list2 = ninegag.grab(site+pageindex,prettyname,str(id+starton),cachePath,site9gagfile,getSetting("cachesites"))
				if list2: list.extend(list2)
			elif 'break' in frame:
				list2 = Break.grab(site+pageindex+str(id+starton),prettyname,cachePath,getSetting("cachesites"))
				if list2: list.extend(list2)				
			else:
				startsection = parameters['startsection']
				endsection = parameters['endsection']
				list2 = grablinks(site+pageindex+str(id+starton),prettyname,startsection,endsection,cachePath,site)
				if list2: list.extend(list2)
	ins.close()
	progress.close()
	unique_stuff = []    
	for item in list:
		if item['url'] not in str(unique_stuff): unique_stuff.append(item)
	return unique_stuff

def grablinks(mainURL,prettyname,sectionstart,sectionend,cachePath,mainsite=None):
	list = []
	html_source_trunk = []
	page = basic.open_url(mainURL)
	try: html_source_trunk = re.findall(sectionstart+'(.*?)'+sectionend, page, re.DOTALL)
	except: pass
	threads = []
	results = []
	for i in range(0, len(html_source_trunk)): 
		print "##funvideos-grablinks: "+html_source_trunk[i]
		if mainsite: pageURL=html_source_trunk[i].replace(mainsite,'').replace('/','').replace('.','').encode('utf-8')
		threads.append(threading.Thread(name=mainURL+str(i),target=grabiframes,args=(html_source_trunk[i],prettyname,cachePath,results,i+1,pageURL, )))	
	[i.start() for i in threads]
	[i.join() for i in threads]
	return results

def grabiframes(mainURL,prettyname,cachePath,results=None,index=None,pageURL=None):
	list = []
	if pageURL: pagecache = os.path.join(cachePath,pageURL)
	if pageURL and getSetting("cachesites") == 'true' and os.path.isfile(pagecache):
		jsonline = basic.readfiletoJSON(pagecache)
		jsonloaded = json.loads(jsonline, encoding="utf-8")
		if index: results.append(jsonloaded)
		else: list.append(jsonloaded)
	else:
		try: page = basic.open_url(mainURL)
		except: 
				page = ' '
				pass
		blocker = re.findall('data-videoid="(.+?)"', page, re.DOTALL)
		if blocker:
			fakeframe = []		
			for videoid in blocker:
				fakeframe.append('<iframe src="http//www.youtube.com/embed/'+videoid+'"</iframe>')
			html = fakeframe
		else: html = re.findall('<iframe(.*?)</iframe>', page, re.DOTALL)
		for trunk in html:
			try: iframe = re.compile('src="(.+?)"').findall(trunk)[0]
			except: 
				try: iframe = re.compile("src='(.+?)'").findall(trunk)[0]
				except: 
					try:iframe = re.compile('data-src="(.+?)"').findall(trunk)[0]
					except: iframe = ''
			if iframe:
				if iframe.find('ad120m.com') > -1 or iframe.find('facebook') > -1 or iframe.find('metaffiliation') > -1 or iframe.find('banner600') > -1 or iframe.find('engine.adbooth.com') > -1 or iframe.find('www.lolx2.com') > -1 or iframe.find('jetpack.wordpress.com') > -1: pass
				else:
					print "##funvideos-grabiframes: "+iframe
					try:
						if iframe.find('youtube') > -1:
							textR,resolver_iframe = youtube_resolver(iframe.replace('-nocookie',''),prettyname,cachePath)
							if resolver_iframe: 	
								if index: results.append(resolver_iframe)
								else: list.append(resolver_iframe)
								if pageURL and getSetting("cachesites") == 'true': basic.writefile(pagecache,'w',textR)
						elif iframe.find('dailymotion') > -1:
							textR,resolver_iframe = daily_resolver(iframe,prettyname,cachePath)
							if resolver_iframe: 							
								if index: results.append(resolver_iframe)
								else: list.append(resolver_iframe)
								if pageURL and getSetting("cachesites") == 'true': basic.writefile(pagecache,'w',textR)
						elif iframe.find('vimeo') > -1:
							textR,resolver_iframe = vimeo_resolver(iframe,prettyname,cachePath)
							if resolver_iframe: 							
								if index: results.append(resolver_iframe)
								else: list.append(resolver_iframe)
								if pageURL and getSetting("cachesites") == 'true': basic.writefile(pagecache,'w',textR)
						elif iframe.find('sapo') > -1:
							textR,resolver_iframe = sapo_resolver(iframe,prettyname,cachePath)
							if resolver_iframe: 							
								if index: results.append(resolver_iframe)
								else: list.append(resolver_iframe)
								if pageURL and getSetting("cachesites") == 'true': basic.writefile(pagecache,'w',textR)
						elif iframe.find('videolog') > -1:
							textR,resolver_iframe = videolog_resolver(iframe,prettyname,cachePath)
							if resolver_iframe: 							
								if index: results.append(resolver_iframe)
								else: list.append(resolver_iframe)
								if pageURL and getSetting("cachesites") == 'true': basic.writefile(pagecache,'w',textR)
					except BaseException as e:
						print '##ERROR-##funvideos-grabiframes: '+iframe+' '+str(e)
			else: print '##ERROR-funvideos:frame on server not supported: '+iframe
	if not index: return list

def sapo_resolver(url,prettyname,cachePath):
	match = re.compile('file=http://.+?/(.+?)/mov/').findall(url)
	if match: 
		videocache = os.path.join(cachePath,str(match[0]))
		if os.path.isfile(videocache):
			jsonline = basic.readfiletoJSON(videocache)
			jsonloaded = json.loads(jsonline, encoding="utf-8")
			return jsonline,jsonloaded
		else:
			try:
				sapoAPI = basic.open_url('http://rd3.videos.sapo.pt/'+match[0]+'/rss2')	
				title = ''
				duration = ''
				thumbnail = ''	
				urlfinal = 	''
				duration = re.compile('<sapo:time>(\d+):(\d+):(\d+)</sapo:time').findall(sapoAPI)
				for horas,minutos,segundos in duration: duration = (int(segundos))+(int(minutos)*60)+(int(horas)*3600)
				thumbnail = re.compile('img src="(.+?)"').findall(sapoAPI)
				title = re.compile('<title>(.+?)</title>').findall(sapoAPI)
				title2 = ''
				title = title[1]
				try: title2 = title.decode('utf8').encode('ascii','xmlcharrefreplace')
				except: pass
				if title2 <> '': title = title2			
				urlfinal = re.compile('<sapo:videoFile>(.+?)</sapo:videoFile>').findall(sapoAPI)
				jsontext = '{"prettyname":"'+prettyname+'","url":"'+urlfinal[0]+'","title":"'+title+'","duration":"'+str(duration)+'","thumbnail":"'+thumbnail[0]+'"}'
				jsonloaded = json.loads(jsontext, encoding="utf-8")
				if getSetting("cachesites") == 'true': basic.writefile(videocache,'w',jsontext.encode('utf8'))
				return jsontext,jsonloaded
			except BaseException as e:
				print '##ERROR-funvideos:sapo_resolver: '+url+' '+str(e)
				pass
	
def youtube_resolver(url,prettyname,cachePath):
	match = re.compile('.*?youtube.com/embed/(.+?)\?').findall(url)
	if not match: match = re.compile('.*?youtube.com/embed/(.*)').findall(url)
	if match:
		videocache = os.path.join(cachePath,str(match[0]))
		if getSetting("cachesites") == 'true' and os.path.isfile(videocache):
			jsonline = basic.readfiletoJSON(videocache)
			jsonloaded = json.loads(jsonline, encoding="utf-8")
			return jsonline,jsonloaded
		else:
			try:
				data=basic.open_url('https://gdata.youtube.com/feeds/api/videos/' + str(match[0]) +'?v2&alt=json')
				parameters = json.loads(data)
				title = ''
				duration = ''
				thumbnail = ''
				title = basic.cleanTitle(parameters['entry']['title']['$t'])
				title2 = ''	
				try: title2 = title.decode('utf8').encode('ascii','xmlcharrefreplace')
				except: title2 = title.encode('ascii','xmlcharrefreplace')
				if title2 <> '': title = title2
				print title
				duration = parameters['entry']['media$group']['yt$duration']['seconds']
				thumbnail = parameters['entry']['media$group']['media$thumbnail'][0]['url']
				jsontext= '{"prettyname":"'+prettyname+'","url":"plugin://plugin.video.youtube/?action=play_video&videoid=' + str(match[0])+'","title":"'+title+'","duration":"'+str(duration)+'","thumbnail":"'+thumbnail+'"}'
				jsonloaded = json.loads('{"prettyname":"'+prettyname+'","url":"plugin://plugin.video.youtube/?action=play_video&videoid=' + str(match[0])+'","title":"'+title+'","duration":"'+str(duration)+'","thumbnail":"'+thumbnail+'"}', encoding="latin-1")
				if getSetting("cachesites") == 'true': basic.writefile(videocache,'w',jsontext)
				return jsontext,jsonloaded
			except BaseException as e:
				print '##ERROR-funvideos:youtube_resolver: '+str(match[0])+' '+str(e)
				pass
    
def daily_resolver(url,prettyname,cachePath):
	if url.find('?') > -1: match = re.compile('/embed/video/(.+?)\?').findall(url)
	else: match = re.compile('/embed/video/(.*)').findall(url)
	if match:
		videocache = os.path.join(cachePath,str(match[0]))
		if getSetting("cachesites") == 'true' and os.path.isfile(videocache):
			jsonline = basic.readfiletoJSON(videocache)
			jsonloaded = json.loads(jsonline, encoding="utf-8")
			return jsonline,jsonloaded
		else:
			try:
				data=basic.open_url('https://api.dailymotion.com/video/' + str(match[0]) +'?fields=title,duration,thumbnail_url,description')
				parameters = json.loads(data)
				title = ''
				duration = ''
				thumbnail = ''
				title = basic.cleanTitle(parameters['title'])
				title2 = ''	
				try: title2 = title.decode('utf8').encode('ascii','xmlcharrefreplace')
				except: pass
				if title2 <> '': title = title2				
				duration = parameters['duration']
				thumbnail = parameters['thumbnail_url']
				jsontext = '{"prettyname":"'+prettyname+'","url":"plugin://plugin.video.dailymotion_com/?mode=playVideo&url=' + str(match[0])+'","title":"'+title.encode('ascii','xmlcharrefreplace')+'","duration":"'+str(duration)+'","thumbnail":"'+thumbnail+'"}'
				jsonloaded = json.loads(jsontext, encoding="utf-8")
				if getSetting("cachesites") == 'true': basic.writefile(videocache,'w',jsontext.encode('utf8'))				
				return jsontext,jsonloaded
			except BaseException as e:
				print '##ERROR-funvideos:daily_resolver: '+str(match[0])+' '+str(e)
				pass

def vimeo_resolver(url,prettyname,cachePath):
	if url.find('?') > -1: match = re.compile('vimeo.com/video/(.+?)\?').findall(url)
	else: match = re.compile('vimeo.com/video/(.*)').findall(url)
	if match:
		videocache = os.path.join(cachePath,str(match[0]))
		if getSetting("cachesites") == 'true' and os.path.isfile(videocache):
			jsonline = basic.readfiletoJSON(videocache)
			jsonloaded = json.loads(jsonline, encoding="utf-8")
			return jsonline,jsonloaded
		else:	
			try:
				data=basic.open_url('http://player.vimeo.com/video/'+str(match[0])+'/config?type=moogaloop&referrer=&player_url=player.vimeo.com&v=1.0.0&cdn_url=http://a.vimeocdn.com')
				parameters = json.loads(data)
				title = ''
				duration = ''
				thumbnail = ''
				title = parameters['video']['title']
				title2 = ''	
				try: title2 = title.decode('utf8').encode('ascii','xmlcharrefreplace')
				except: pass
				if title2 <> '': title = title2				
				duration = parameters['video']['duration']
				thumbnail = parameters['video']['thumbs']['640']
				try: url = parameters['request']['files']['h264']['hd']['url']
				except: url = parameters['request']['files']['h264']['sd']['url']
				jsontext = '{"prettyname":"'+prettyname+'","url":"' + url +'","title":"'+title.encode('ascii','xmlcharrefreplace')+'","duration":"'+str(duration)+'","thumbnail":"'+thumbnail+'"}'
				jsonloaded = json.loads(jsontext, encoding="utf-8")
				if getSetting("cachesites") == 'true': basic.writefile(videocache,'w',jsontext.encode('utf8'))
				return jsontext,jsonloaded
			except BaseException as e:
				print '##ERROR-funvideos:vimeo_resolver: '+str(match[0])+' '+str(e)
				pass

def videolog_resolver(url,prettyname,cachePath):
	try:
		ID = re.compile('id_video=(.+?)&amp').findall(url[0])
		videoID = ID[0]		
		videocache = os.path.join(cachePath,str(videoID))
		if getSetting("cachesites") == 'true' and os.path.isfile(videocache):
			jsonline = basic.readfiletoJSON(videocache)
			jsonloaded = json.loads(jsonline, encoding="utf-8")
			return jsonline,jsonloaded
		else:
			content = abrir_url("http://videolog.tv/"+videoID)
			match = re.compile('<meta property="og:image" content="http://videos.videolog.tv/(.+?)/(.+?)/g_'+id+'_\d+').findall(content)
			image = re.compile('<meta property="og:image" content="(.+?)">').findall(content)
			title = re.compile('<meta property="og:title" content="(.+?)">').findall(content)
			title = basic.cleanTitle(title[0])
			title2 = ''	
			try: title2 = title.decode('utf8').encode('ascii','xmlcharrefreplace')
			except: pass
			if title2 <> '': title = title2			
			url='http://videos.videolog.tv/'+match[0]+'/'+match[1]+'/'+id+'.mp4'
			jsontext = '{"prettyname":"'+prettyname+'","url":"' + url +'","title":"'+title.encode('ascii','xmlcharrefreplace')+'","duration":"60","thumbnail":"'+image[0]+'"}'
			jsonloaded = json.loads(jsontext, encoding="utf-8")
			if getSetting("cachesites") == 'true': basic.writefile(videocache,'w',jsontext.encode('utf8'))			
			return jsontext,jsonloaded
	except BaseException as e:
		print '##ERROR-funvideos:videolog_resolver: '+str(id)+' '+str(e)
		pass
		
def send_email(name,url):
	import smtplib
	name = name.split(' [')[0]
	if 'dailymotion' in url: url = url.replace('plugin://plugin.video.dailymotion_com/?mode=playVideo&url=','http://www.dailymotion.com/video/')
	elif 'youtube' in url: url = url.replace('plugin://plugin.video.youtube/?action=play_video&videoid=','https://www.youtube.com/watch?v=')
	elif 'break' in url:
		videoid = url.split('/')[7]
		pageid = url.split('/')[8]
		pageid = re.compile('(.+?)-\d+_kbps.').findall(pageid)[0]
		url = 'http://www.break.com/video/%s-%s' % (pageid,videoid)
	mail_user = getSetting("fromemail")
	mail_pwd = getSetting("password")
	FROM = getSetting("fromemail")
	try: TO = getSetting("toemail").split(',')
	except: TO = [getSetting("toemail")]
	SUBJECT = name
	TEXT = url
	# Prepare actual message
	message = """\From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
	try:
		if getSetting("server") == 'Gmail': server = smtplib.SMTP("smtp.gmail.com", 587)
		elif getSetting("server") == 'Hotmail': server = smtplib.SMTP("smtp.live.com", 587)
		server.ehlo()
		server.starttls()
		server.login(mail_user, mail_pwd)
		server.sendmail(FROM, TO, message)
		server.close()
		print 'successfully sent the mail'
	except: print "failed to send mail"