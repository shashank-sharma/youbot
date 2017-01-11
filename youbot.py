'''


###    ##    #########
###    ##    ##       #
 ###  ##     ##       #
   ###       #########
   ###       ##       #
   ###       #########

YouBot - by Shashank Sharma


#issue1 : youwatch not working ... Done

'''
from __future__ import unicode_literals
import requests
import os
from bs4 import BeautifulSoup
import youtube_dl
import time

def youtubeWatch(name):
	url = "https://www.youtube.com/results?search_query="
	print 'Before adding let me verify .',
	name = name.replace(' ','+')
	print name
	try:
		r = requests.get(url+name)
	except:
		print 'nooooooooo'
	soup = BeautifulSoup(r.content)
	user = soup.find_all('a',{'class': 'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 g-hovercard yt-uix-sessionlink      spf-link '})
	print user
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

def createDatabase():
	print '\n[youbot]: OK '+uname+' Let\'s get started by creating your database'
	time.sleep(4)
	print '[youbot]: Our database consist of many .txt files so don\'t panic. You can later find it why are they used.'
	time.sleep(7)
	print '[youbot]: Let\s get started. Please enter your favourite channel names.'
	time.sleep(5)
	print '[youbot]: If you don\'t want to type then simply press enter key'
	yname = raw_input()
	if yname == '':
		print '[youbot]: 0 Favourites channel'
	else:
		youtubeWatch(yname)

def urlHelp():
	print '[youbot]: Lets talk about how to download videos and audios'
	time.sleep(3)
	print '[youbot]: To download video use this format "v (url)"'
	time.sleep(3)
	print '[youbot]: And to download audio use "a (url)"'
	time.sleep(3)
	print '[youbot]: Videos will be downloaded in your local storage where this program is.'

def remindHelp():
	print '[youbot]: Sorry for taking this much of time, Now one last step'
	time.sleep(6)
	print 'To get remainder for any particular channel just type "remind (channel_name)"'
	time.sleep(4)
	print 'NOTE: channel_name have to be exactly same'

print '[youbot]: Lets get started by knowing whats your name'
time.sleep(2)
print '[youbot]: Please enter your name :',
uname = raw_input('>>>')
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
	print '[youbot]: That\'s it I can do this much till now'
if comm == 'skip' or comm == 'youbot':
	time.sleep(4)
	print '-------------sleep4'
	createDatabase()
	print '----------------database ban gaya'
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