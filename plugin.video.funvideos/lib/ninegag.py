# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import os,json,re
import basic

def grab(url,prettyname,id,cachePath,site9gagfile,cacheE):
	jsondata = []
	list = []
	line = basic.readoneline(site9gagfile)
	idpage = re.findall('::'+id+'::::(.+?)::', line, re.DOTALL)
	if not idpage: page = basic.open_url('http://9gag.tv')
	else: page = basic.open_url(url+idpage[0],'9gag')
	jsondata = re.findall('   postGridPrefetchPosts = (.+?)];', page, re.DOTALL)
	j = json.loads(jsondata[0]+']')
	size = len(j)
	e=0
	for data in j:
		e = e + 1
		if e == size:
			line = basic.readoneline(site9gagfile)
			if not '<'+id+'>' in line: basic.writefile(site9gagfile,"a",'::'+str(int(id)+1)+'::::'+data['prevPostId']+'::') 
		try:
			duration = 0
			time = re.findall('PT(\d+)M(\d+)S', data['videoDuration'], re.DOTALL)
			if time:
				for min,sec in time: duration = int(min)*60+int(sec)
			else:
				time = re.findall('PT(\d+)M', data['videoDuration'], re.DOTALL)
				if time: duration = int(time[0])*60
				else:
					time = re.findall('PT(\d+)S', data['videoDuration'], re.DOTALL)
					if time: duration = time[0]
		except: 
			duration = 60
			pass
		title = basic.cleanTitle(data['ogTitle'])	
		videocache = os.path.join(cachePath,data['videoExternalId'])
		jsontext = '{"prettyname":"'+prettyname+'","url":"plugin://plugin.video.youtube/?action=play_video&videoid=' +data['videoExternalId']+'","title":"'+title.encode('ascii','xmlcharrefreplace')+'","duration":"'+str(duration)+'","thumbnail":"'+data['thumbnail_360w']+'"}'
		jsonloaded = json.loads(jsontext, encoding="utf-8")
		if cacheE == 'true' and not os.path.isfile(videocache): basic.writefile(videocache,'w',jsontext.encode('utf8'))
		list.append(jsonloaded)
	return list 
