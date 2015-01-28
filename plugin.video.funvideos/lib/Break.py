# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import os,json,re
import basic

def grab(url,prettyname,cachePath,cacheE):
	list = []
	try:
		page = basic.open_url(url)
		page = page.replace("\\","")
		ids = re.findall('data-content-id="(\d+)"', page, re.DOTALL)
		for videoid in ids:
			videocache = os.path.join(cachePath,str(videoid))
			if cacheE == 'true' and os.path.isfile(videocache):
				jsonline = basic.readfiletoJSON(videocache)
				jsonloaded = json.loads(jsonline, encoding="utf-8")			
			else:
				content = basic.open_url("http://www.break.com/embed/"+videoid)
				matchAuth=re.compile('"AuthToken": "(.+?)"', re.DOTALL).findall(content)
				matchURL=re.compile('"uri": "(.+?)".+?"height": (.+?),', re.DOTALL).findall(content)
				matchYT=re.compile('"youtubeId": "(.*?)"', re.DOTALL).findall(content)
				title=re.compile('"contentName": "(.+?)",', re.DOTALL).findall(content)
				title = basic.cleanTitle(title[0])
				title2 = ''				
				try: title2 = title.decode('utf8').encode('ascii','xmlcharrefreplace')
				except: pass
				if title2 <> '': title = title2		
				duration=re.compile('"videoLengthInSeconds": "(\d+)",', re.DOTALL).findall(content)	
				thumb = re.compile('"thumbUri": "(.+?)",', re.DOTALL).findall(content)				
				finalUrl=""
				if matchYT and matchYT[0]!="":
					finalUrl = "plugin://plugin.video.youtube/?action=play_video&videoid=" + matchYT[0]
					videocache2 = os.path.join(cachePath,str(matchYT[0]))	
					if cacheE == 'true' and not os.path.isfile(videocache): 
						jsontext = '{"prettyname":"'+prettyname+'","url":"'+finalUrl+'","title":"'+title+'","duration":"'+str(duration[0])+'","thumbnail":"'+thumb[0]+'"}'
						jsonloaded = json.loads(jsontext, encoding="utf-8")			
						basic.writefile(videocache2,'w',jsontext.encode('utf8'))
				else:
					max=0
					for url, height in matchURL:
						height=int(height)
						if height>max: 
							finalUrl=url.replace(".wmv",".flv")+"?"+matchAuth[0]
							max=height
				jsontext = '{"prettyname":"'+prettyname+'","url":"'+finalUrl+'","title":"'+title+'","duration":"'+str(duration[0])+'","thumbnail":"'+thumb[0]+'"}'
				jsonloaded = json.loads(jsontext, encoding="utf-8")
				if cacheE == 'true' and not os.path.isfile(videocache): basic.writefile(videocache,'w',jsontext.encode('utf8'))
			list.append(jsonloaded)
		return list
	except BaseException as e:
		print '##ERROR-funvideos:Break_resolver: '+url+' '+str(e)