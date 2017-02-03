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
#issue3 : remind free code camp will not work. Make it work soon ... Removed
#issue4 : Download + Buffer video ... Failed

'''
from __future__ import unicode_literals
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

try:
	import requests
	import os
	from bs4 import BeautifulSoup
	import youtube_dl
	import time
	from random import randint
	print bcolors.OKGREEN+'Import: OK'+bcolors.ENDC
except:
	print bcolors.FAIL+'Import: FAILED'+bcolors.ENDC
time.sleep(1)



def buffer(title):
	p = subprocess.Popen(["/usr/bin/vlc", title+'.mp4'])
	time.sleep(3)
	print bcolors.FAIL+'\n\nEXIT VLC TO QUIT'+bcolors.ENDC

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
	print bcolors.FAIL+'   ####    ##    ##########'+bcolors.ENDC
	print bcolors.FAIL+'   ####    ##    ###       #'+bcolors.ENDC
	print bcolors.FAIL+'    ####  ##     ###      #'+bcolors.ENDC
	print bcolors.FAIL+'      ####       ##########'+bcolors.ENDC
	print bcolors.FAIL+'      ####       ###       #'+bcolors.ENDC
	print bcolors.FAIL+'      ####       ##########'+bcolors.ENDC

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
			video_title = info_dict.get('title', None)
			#print video_title
			#buffer(video_title)
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
			print '[youbot]:'+bcolors.OKGREEN+' Found '+temp[2]+bcolors.ENDC
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
			print bcolors.OKGREEN+'\n\n[youbot]: Channel Successfully updated in your local system'+bcolors.ENDC
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
	url = urls+'/videos'
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
	print '[youbot]: My name is Youbot and I will help you with all the stuff related youtube'
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
		print '[youbot]: 6. If you are bored then I can give you some random video suggesition'
		time.sleep(6)
		print '[youbot]: 7. You can search any playlist from here and make them download instantly.'
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
	if num == 0:
		name = fav
	else:
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
			print bcolors.FAIL+'\n\nNo new Update'+bcolors.ENDC
			break
		else:
			print bcolors.OKGREEN+'[Update]: http://www.youtube.com'+i['href']+bcolors.ENDC
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
			if fav[i] == name[1]:
				channelRemind(0,name[1])
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
	print '[youbot]: type "add (url)" - Add youtube url to download stack'
	print '[youbot]: type "download v (url)" - download video'
	print '[youbot]: type "download a (url)" - download audio'
	print '[youbot]: type "download pv (url)" - download playlist video'
	print '[youbot]: type "download pa (url)" - download playlist in audio'
	print '[youbot]: type "addchannel (channel-name)" to add channel to your favourites'
	print '[youbot]: type "remind" to get all favourite channel list'
	print '[youbot]: type "trending" to get all trending videos available'
	print '[youbot]: type "random" to get any 1 random video'
	print '[youbot]: type "delete" to erase everything. Yes Everything'
	print '[youbot]: type "psearch (name) to search playlist related query'

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
		print '\n'
		print '[youbot]'+str(x)+' '+i['title']
		print '[youbot] Link: '+ 'https://www.youtube.com'+i['href']
		if x%5 == 0:
			ke = raw_input('Enter any key proceed else enter quit')
			if ke == 'quit':
				break
		x+=1
	print '[youbot]: Total videos found: '+str(x)
	files.close()
	file.close()

def randomVideo():                                         # Need best practice for this
	print 'Generating any random video'
	r = requests.get('https://www.youtube.com/feed/trending')
	soup = BeautifulSoup(r.content)
	l = soup.find_all("a",{"class": 'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink      spf-link '})
	file = open('random.txt','w+')
	files = open('random-url.txt','w+')
	x = 1
	for i in l:
		try:
			file.write(str(i['title'])+'\n')
		except:
			file.write('Unknown text'+'\n')
		files.write(str(i['href'])+'\n')
	files.close()
	file.close()

	file = open('random.txt','r')
	uname = file.read().splitlines()
	file.close()
	files = open('random-url.txt','r')
	uurl = files.read().splitlines()
	files.close()
	nu = randint(0,len(uname))
	print '\n\n[youbot]: '+uname[nu]
	print '[youbot]: https://www.youtube.com'+uurl[nu]

def addUrl(url):

	file = open('url-stack.txt','a+')
	print '[youbot]: Verifying given URL'
	try:
		r = requests.get(url)
		file.write(url+'\n')
		print 'Successfully added'
	except:
		print '[youbot]: URL is not valid'

def downloadUrl():

	file = open('url-stack.txt','r')
	uname = file.read().splitlines()
	file.close()
	print '[youbot]: Currently in total you have '+str(len(uname))+' videos available'
	print '[youbot]: Downloading . . .'
	for i in uname:
		ytDownload(i)

def playlistSearch(name):
	name = '+'.join(name[1:])
	url = 'https://www.youtube.com/results?q='+name+'&sp=CAMSAhAD'
	r = requests.get(url)
	soup = BeautifulSoup(r.content)
	l = soup.find_all("a",{"class": "yt-uix-sessionlink       spf-link "})
	m = soup.find_all("a",{"class": "yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink      spf-link "})
	print '[youbot]: '+str(len(l))+' Results found:\n'
	for i in xrange(len(l)):
		print '[youbot]: '+m[i].text
		print l[i].text
		print 'https://www.youtube.com'+l[i]['href']
		print '\n'
		if (i+1)%5 == 0:
			a = raw_input('Press Enter to show more')

#if not os.path.isfile('./user.txt'):
#	uname = intro()
try:
	file = open('user.txt','r')
	uname = file.read().splitlines()
	file.close()
	print bcolors.OKGREEN+'Session found: '+uname[0]+bcolors.ENDC
	time.sleep(1)
except:
	print bcolors.OKGREEN+'New Session found'+bcolors.ENDC
	time.sleep(1)
	uname = intro()
print '\n\n\n'
logo()
print '\n\n\n'
print 'Welcome back master '+uname[0]
while True:
	print bcolors.FAIL+'[youbot]: '+bcolors.ENDC,
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
	elif inp[0] == 'random':
		randomVideo()
	elif inp[0] == 'delete':
		txtDelete()
	elif inp[0] == 'add':
		addUrl(inp[1])
	elif inp[0] == 'download-list':
		downloadUrl()
	elif inp[0] == 'psearch':
		playlistSearch(inp)
	else:
		print '[youbot]: Seems like you are lost! Say "bot-help" and I will come to save you :D'
