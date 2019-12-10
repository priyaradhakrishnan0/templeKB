#Scrap webpages for templeKB
# encoding=utf8
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

import requests
import os
from bs4 import BeautifulSoup
from KGconfig import *
import re

#Scrape the URL and create templeNmae.txt and update metadata
def scrape(URL):
	#URL = 'http://www.vaikhari.org/kurinjikkavu.html' #'http://www.vaikhari.org/aniyur.html'#'http://www.vaikhari.org/kumaranalloor.html'#'http://www.vaikhari.org/thirunavaya.html'#'http://www.vaikhari.org/thirumittakkod.html' #'http://www.vaikhari.org/thrikkakara.html'#'http://www.vaikhari.org/thiruvattar.html'#'http://www.vaikhari.org/thiruvalla.html'#'http://www.vaikhari.org/thirupatisaram.html'
	#'http://www.vaikhari.org/kanyakumari.html' #'http://www.vaikhari.org/thiruvaranmula.html' #'http://www.vaikhari.org/mulakkulam.html'
	r = requests.get(URL)
	soup = BeautifulSoup(r.content, 'html5lib', from_encoding="utf-8")
	#print(soup.prettify())

	title = soup.find('title')
	#print(title)
	if 'http://www.vaikhari.org/' in URL:
		if title == None:
			title = soup.find('strong')
		if title == None:
			title = soup.find('b')

	templeName = None
	if title:
		print(title.string)
		templeName = title.string.strip()+'.txt'  
		if 'https://www.indianmirror.com/' in URL:
			templeName = title.string.split(',')[0]+'.txt'
		#templeName='Mulaykkode Sree Dharma Sastha Temple.txt'
		print(templeName)

		with open(os.path.join(args['web_scraped_temple_text_path'],templeName), 'w+', encoding='utf-8') as wf:
			for line in soup.get_text().split('\n'):
				if len(line.split()) > 7:
					wf.write(line+'\n')

		with open('data/web_corpus_met_data.csv','a') as md:
		    md.write('\n'+templeName+';'+URL)

	return templeName

def main():
	print(args['url'])
	#URL = 'http://www.vaikhari.org/kurinjikkavu.html'
	scrape(args['url'])

	Tirumala Tirupati Devasthanams(TTD)



if __name__ == '__main__':
    main()
