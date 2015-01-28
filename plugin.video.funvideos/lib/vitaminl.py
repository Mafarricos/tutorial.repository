# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import os,json,re
import basic

def grab(url,prettyname,cachePath,cacheE):
	list = []
	try:
		content = basic.open_url(url)
		spl = content.split('<div class="videoListItem">')
		for i in range(1, len(spl), 1):
			entry = spl[i]
			match = re.compile('data-youtubeid="(.+?)"', re.DOTALL).findall(entry)
			id = match[0]
			match = re.compile('<div class="duration">(.+?)</div>', re.DOTALL).findall(entry)
			duration = match[0].strip()
			splDuration = duration.split(":")
			duration = str(int(splDuration[0])*60+int(splDuration[1]))
			thumb = "http://img.youtube.com/vi/"+id+"/0.jpg"
			match = re.compile('alt="(.+?)"', re.DOTALL).findall(entry)
			title = match[0]
			title = basic.cleanTitle(title)
			videocache = os.path.join(cachePath,str(id))
			title2 = ''		
			try: title2 = title.decode('utf8').encode('ascii','xmlcharrefreplace')
			except: pass
			if title2 <> '': title = title2
			jsontext = '{"prettyname":"'+prettyname+'","url":"plugin://plugin.video.youtube/?action=play_video&videoid=' + str(id)+'","title":"'+title+'","duration":"'+str(duration)+'","thumbnail":"'+thumb+'"}'
			jsonloaded = json.loads(jsontext, encoding="utf-8")
			if cacheE == 'true' and not os.path.isfile(videocache): basic.writefile(videocache,'w',jsontext.encode('utf8'))
			list.append(jsonloaded)
		if list: return list
	except BaseException as e:
		print '##ERROR-funvideos:VitaminL_resolver: '+url+' '+str(e)
		pass
