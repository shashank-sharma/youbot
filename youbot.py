'''


####    ##    ##########
####    ##    ###       #
 ####  ##     ###      #
   ####       ##########
   ####       ###       #
   ####       ##########

YouBot - by Shashank Sharma


#issue1 : youwatch not working ... Done
#issue2 : remind function taking input ... Done

'''
from __future__ import unicode_literals
import requests
import os
from bs4 import BeautifulSoup
import youtube_dl
import time

def txtDelete():
	print '\n\n'
	print '[youbot]: You are trying to remove some part of my memory from your local storage.'
	print '[youbot]: This command will delete ALL .txt file present in that directory. Make sure your program is isolated in seperate folder'
	a = raw_input('[youbot]: Type "Y" to delete else "N": ')
	if a == 'y' or a == 'Y':
		filelist = [ f for f in os.listdir(".") if f.endswith(".txt") ]
		x = 0
		for f in filelist:
			x+=1
			print '[youbot]: Deleting: ' ,f
			os.remove(f)
		print '\n[youbot]: Successfuly deleted '+str(x)+' files'
	else:
		print 'Wise decision!'

def logo():
	print '   ####    ##    ##########'
	print '   ####    ##    ###       #'
	print '    ####  ##     ###      #'
	print '      ####       ##########'
	print '      ####       ###       #'
	print '      ####       ##########'

def getPlayList(choice):
	# If URL is taken while watching from playlist then it will get real link.
	url = str(choice[2])
	print '[youtube]: Opening playlist page',
	if '&' in url:
		url = url.split('&')
		url = "https://www.youtube.com/playlist?"+url[1]
	try:
		r = requests.get(url)
	except:
		print('[youbot]: Not able to start internet for surfing')
	soup = BeautifulSoup(r.content)
	print 'Done'
	links = soup.find_all("a",{"class": "pl-video-title-link yt-uix-tile-link yt-uix-sessionlink  spf-link "})
	count = 0
	file = open("youtube-links.txt","w")
	for i in links:
		url = str(i['href'])
		url = url.split('&')
		file.write("https://www.youtube.com%s\n" % url[0])
		count+=1
	file.close()
	print('[youbot]: '+str(count)+' links found')
	print('[youbot]: All links are saved in youtube-links.txt')
	print("[youbot]: Enter those numbers which you don't want to download like: 1 2 3 else type 0")
	ignore = map(int, raw_input().split())
	x = 1
	file = open("youtube-links.txt","r")
	completed = 0
	for i in file:
		if x in ignore:
			print ('[youbot]: download '+ str(x)+'/'+str(count)+'] : Skip')
    	else:
        	print ('[youbot]: download '+ str(x)+'/'+str(count)+']')
        	if choice[1][1] == 'v':
        		completed += ytDownload(i)
        	elif choice[1][1] == 'a':
        		completed += ytAudio(i)
    	x+=1
	file.close()
	print('\n\n\n[youbot]: Completed '+str(completed)+'/'+str(count-len(ignore)))

def ytDownload(link):
	try:
		r = requests.get(link)
		ydl_opts = {}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([link])
		print '[youbot]: Downloaded'
		return 1
	except:
		print '[youbot]: Wrong link'
		return 0

def ytAudio(link):
	try:
		ydl_opts = {
			'format': 'bestaudio/best',
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}],
		}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([link])
		return 1
	except:
		return 0

def urlDownload(aurl):
	if aurl[1][0] == 'p':
		getPlayList(aurl)
	elif aurl[1][0] == 'v':
		ytDownload(str(aurl[2]))
	elif aurl[1][0] == 'a':
		ytAudio(str(aurl[2]))
	else:
		print '[youbot]: Wrong syntax . . . Try again'


def youtubeWatch(name):
	url = "https://www.youtube.com/results?search_query="
	print 'Before adding let me verify .',
	name = name.replace(' ','+')
	print name
	try:
		r = requests.get(url+name)
		print '.',
	except:
		print 'Failed'
	soup = BeautifulSoup(r.content)
	user = soup.find_all('a',{'class': 'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 g-hovercard yt-uix-sessionlink      spf-link '})
	print '.'
	for i in user:
		temp = i['href']
		temp = temp.split('/')
		if temp[1] == 'user' or temp[1] == 'channel':
			urls = 'http://www.youtube.com'+str(i['href'])
			print '[youbot]: Found ',temp[2]
			print '[youtube]: Let\' prepare your data'
			newChannel(name)
			print '\n\n[youbot] 2/5 Let\'s get some data related video',
			li = getLink(name,urls)
			print '  Done'
			print '\n\n[youbot] 3/5 Let me update your content',
			updateContent(li,name)
			print '  Done'
			print '\n\n[youbot] 4/5 Let me update your links',
			updateLink(li,name)
			print '  Done'
			print '\n\n[youbot]: Channel Successfully updated in your local system'
			favouriteList(name)
		else:
			print 'Error not found'
			break

def favouriteList(name):
	print '[youbot]: 5/5 Adding this channel to your favourites',
	file = open('favourite.txt','a')
	file.write(name+'\n')
	file.close()
	print '  Done'

def updateLink(l,name):
	file = open(name+'-link.txt','w')
	for i in l:
		temp = i['href']
		temp = str(temp)
		file.write(temp+'\n')
	file.close()

def updateContent(l,name):
	file = open(name+'.txt','w')
	for i in l:
		temp = i['title']
		try:
			temp = str(temp)
		except:
			temp = 'Error occured'
		file.write(temp+'\n')
	file.close()

def getLink(name,urls):
	file = open('youtube-channel.txt','a')
	file.write(urls+'\n')
	file.close()
	url = urls
	print url
	ch = requests.get(url)

	soup = BeautifulSoup(ch.content)
	l = soup.find_all("a",{"class": "yt-uix-sessionlink yt-uix-tile-link  spf-link  yt-ui-ellipsis yt-ui-ellipsis-2"})
	return l

def newChannel(name):
	print '\n\n[youbot] 1/5 Creating your database'
	file = open(name+'.txt','w')
	file.close()
	file = open(name+'-link.txt','w')
	file.close()
	print '[youbot]: '+name+'.txt have been created'
	print '[youbot]: '+name+'-link.txt have been created' 
	if not os.path.isfile('./'+name+'.txt') and not os.path.isfile('./youtube-channel.txt'):
		file = open('favourite.txt','w')
		file.close()
		file = open('youtube-channel.txt','w')
		file.close()
		print '[youbot]: favourite.txt have been created'
	print 'Done'

def createDatabase(uname):
	print '\n[youbot]: OK '+uname+' Let\'s get started by creating your database'
	time.sleep(4)
	print '[youbot]: Our database consist of many .txt files so don\'t panic. You can later find it why are they used.'
	time.sleep(7)
	print '[youbot]: Let\'s get started. Please enter your favourite channel names.'
	time.sleep(5)
	print '[youbot]: If you don\'t want to type then simply press enter key'
	yname = raw_input()
	if yname == '':
		print '[youbot]: 0 Favourites channel'
	else:
		while True:
			youtubeWatch(yname)
			print '[youbot]: Type bot-quit if you have no channels to add'
			print '[youbot]: Any more channels: ',
			yname = raw_input()
			if yname == 'bot-quit':
				break

def urlHelp():
	print '[youbot]: Lets talk about how to download videos and audios'
	time.sleep(3)
	print '[youbot]: To download video use this format "vdownload (url)"'
	time.sleep(3)
	print '[youbot]: And to download audio use "adownload (url)"'
	time.sleep(3)
	print '[youbot]: Add p in front of commands to download playlist example "pvdownload (url)" for videos same for audio "padownload (url)"'
	time.sleep(7)
	print '[youbot]: Videos will be downloaded in your local storage where this program is.'

def remindHelp():
	print '[youbot]: Sorry for taking this much of time, Now one last step'
	time.sleep(6)
	print '[youbot]: To get remainder for any particular channel just type "remind (channel_name)"'
	time.sleep(4)
	print '[youbot]: NOTE: channel_name have to be exactly same'

def intro():
	print '[youbot]: Welcome to Youbot BETA v1.0'
	print '[youbot]: "Your smart bot"'
	time.sleep(3)
	print '[youbot]: Lets get started by knowing whats your name'
	time.sleep(2)
	print '[youbot]: Please enter your name :'
	uname = raw_input('>>>')
	file = open("user.txt","a+")
	file.write(uname)
	file.close()
	print '[youbot]: '+uname+' Nice!  Youbot <3 '+uname
	time.sleep(3)
	print '[youbot]: Since you are new here so lets get familiar that who I am'
	time.sleep(5)
	print '[youbot]: My name is Youbot and I will help you with all the stuff'
	time.sleep(5)
	print '[youbot]: Since my developer is not that professional that\'s why i can do few stuff only'
	time.sleep(5)
	print '[youbot]: Type "youbot" so that I can tell you what I can do else type "skip"'
	comm = raw_input('>>>')
	if comm == 'youbot':
		print '[youbot]: 1. I can download any Youtube video easily.'
		time.sleep(4)
		print '[youbot]: 2. I can download any Youtube playlist all you need to do is paste link which was having those playlist on side.'
		time.sleep(6)
		print '[youbot]: 3. I can download Youtube video in audio format and also from playlist. Its like 100 videos = 100 audio songs.'
		time.sleep(6)
		print '[youbot]: 4. I can remind you if there is any latest upload by any youtube channel or not.'
		time.sleep(6)
		print '[youbot]: 5. I can show you all trending videos quickly.'
		time.sleep(6)
		print '[youbot]: That\'s it I can do this much till now'
	if comm == 'skip' or comm == 'youbot':
		time.sleep(4)
		createDatabase(uname)
		time.sleep(2)
		urlHelp()
		time.sleep(6)
		remindHelp()
		time.sleep(5)
		print '[youbot]: That\'t it. You are now all set for using this program. Congratulations :D'
		time.sleep(5)
		print '[youbot]: If you need any help then type "youbot" and i will come again'
	else:
		print '[youbot]: I have faith in you. Please type it correctly'
	return uname

def channelRemind(num,fav):
	name = fav[num-1]
	file = open('youtube-channel.txt','r')
	yc = file.read().splitlines()
	file.close()
	print '[youtube]: Getting updates for '+name
	el = getLink(name,yc[num-1])
	file = open(name+'-link.txt','r')
	sear = file.read().splitlines()
	file.close()
	file = open(name+'.txt','r')
	sear1 = file.read().splitlines()
	file.close()
	sn = 0
	for i in el:
		if sear[sn] == i['href']:
			print 'No new Update'
			break
		else:
			print '[Update]: http://www.youtube.com/'+i['href']
		sn+=1

	print '\n\n Have look at previous latest videos :\n'
	sn = 1
	for i in xrange(3):
		print str(sn)+' '+sear1[i]+'	 || 	'+'http://www.youtube.com'+sear[i]
		sn+=1


def remind(name):
	num = 0
	if len(name) == 2:
		file = open('favourite.txt','r')
		fav = file.read().splitlines()
		file.close()
		for i in xrange(len(fav)):
			if fav[i] == name:
				channelRemind(i,name)
				num = -1

	else:
		try:
			file = open('favourite.txt','r')
			fav = file.read().splitlines()
			file.close()
			file = open('youtube-channel.txt','r')
			yc = file.read().splitlines()
			file.close()
			print 'Favourite list: '
			x = 1
			for i in fav:
				print str(x),' ',i
				x+=1
			print 'Enter serial number that you want remind else type 0'
			num = int(raw_input())
		except:
			print '[youbot]: Nothing to remind. Type addchannel (channel-name) to add some channel'
	if num != 0:
		channelRemind(num,fav)
	elif num == 0:
		print 'Quitting'
	elif num != -1:
		print 'Error not found'

def commandHelp():
	print '[youbot]: Bot reporting for duty'
	print '[youbot]: type "download v (url)" - download video'
	print '[youbot]: type "download a (url)" - download audio'
	print '[youbot]: type "download pv (url)" - download playlist video'
	print '[youbot]: type "download pa (url)" - download playlist in audio'
	print '[youbot]: type "addchannel (channel-name)" to add channel to your favourites'
	print '[youbot]: type "find" to find any random video'
	print '[youbot]: type "remind" to get all favourite channel list'
	print '[youbot]: type "trending" to get all trending videos available'

def trending():
	print "[youbot]: Let's see what is trending"
	url = 'https://www.youtube.com/feed/trending'
	r = requests.get(url)
	soup = BeautifulSoup(r.content)
	l = soup.find_all("a",{"class": 'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink      spf-link '})
	print '[youbot]: Creating file trending-name.txt'
	file = open('trending-name.txt','a+')
	print '[youbot]: Creating file trending-url.txt'
	files = open('trending-url.txt','a+')
	x = 1
	for i in l:
		try:
			file.write(str(i['title'])+'\n')
		except:
			file.write('Unknown text'+'\n')
		files.write(str(i['href'])+'\n')
		print str(x)+' '+i['title']
		print '[youbot] Link: '+ 'https://www.youtube.com'+i['link']
		if x%5 == 0:
			ke = raw_input('Enter any key proceed else enter quit')
			if ke == 'quit':
				break
		x+=1
	print '[youbot]: Total videos found: '+str(x)
	files.close()
	file.close()

#if not os.path.isfile('./user.txt'):
#	uname = intro()
try:
	file = open('user.txt','r')
	uname = file.read().splitlines()
	file.close()
except:
	uname = intro()
print '\n\n\n'
logo()
print '\n\n\n'
while True:
	print '[youbot]: ',
	inp = raw_input()
	inp = inp.split(' ')
	if inp[0] == 'bot-help':
		commandHelp()
	elif inp[0] == 'download':
		urlDownload(inp)
	elif inp[0] == 'trending':
		trending()
	elif inp[0] == 'remind':
		remind(inp)
	elif inp[0] == 'addchannel':
		youtubeWatch(inp[1])
	elif inp[0] == 'bot-exit':
		print 'Bye'
		exit()
	elif inp[0] == 'delete':
		txtDelete()
	else:
		print '[youbot]: Seems like you are lost! Say "bot-help" and I will come to save you :D'