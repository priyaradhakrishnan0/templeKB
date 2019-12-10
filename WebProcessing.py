#Web scraped temple text processing
import json
import os
import re

from KGconfig import *

def getWebFile():
	for webFil in os.listdir(args['web_scraped_temple_text_path']):
		if not webFil.startswith('.'):
			yield webFil

def getWebText(webFile):
	data = []
	with open(os.path.join(args['web_scraped_temple_text_path'],webFile)) as wf:
		for line in wf:
			clean_line = re.sub(r'[^a-zA-Z0-9.,;\'\" ]',' ',line)
			data.append(clean_line)

	print('Retrieved '+str(len(data))+' lines from web scraping File '+webFile)
	return ' '.join(data)
'''
def main()
	webFile = getWebFile()
	for webScrapFile in webFile: #get value yielded
		print(getWebText(webScrapFile))
'''
