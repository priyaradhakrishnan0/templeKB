#Wiki annotated corpus processing
import json
import os

from KGconfig import *

def printWikiFile(wikiDir,wikiFilePath):
	data = []
	with open(os.path.join(wiki_corpus_path,wikiDir,wikiFilePath)) as wf:
		for line in wf:
			data.append(json.loads(line))
	for line in data: 
		print(data[0]) 
		print(data[0]['url'])
		print(data[0]['id'])
		print(len(data[0]['text'])) 
		print(data[0]['annotations'][0])
		print(data[0]['annotations'][0]['surface_form'])
		break

#Returns one title or empty dict
def getArticleText2(qtitle, wikiDir, wikiFilePath):	
	text_data = dict()
	with open(os.path.join(args['wiki_corpus_path'],wikiDir,wikiFilePath)) as wf:
		data = []
		for line in wf:
			data.append(json.loads(line))
			for i,line in enumerate(data): #print(data[i]['text'])
				art_title = ''.join(data[i]['url'].split('/')[-1:])
				if art_title==qtitle:
					text_data[art_title] = data[i]['text']
					break 

			if len(text_data) > 0:
				return text_data

	#print('Returning '+str(len(text_data))+' articles from wikiFile '+wikiDir+'/'+wikiFilePath)
	return text_data

def getArticleText(wikiDir,wikiFilePath):
	data = []
	text_data = dict()
	with open(os.path.join(args['wiki_corpus_path'],wikiDir,wikiFilePath)) as wf:
		for line in wf:
			data.append(json.loads(line))
	for i,line in enumerate(data): #print(data[i]['text'])
		text_data[''.join(data[i]['url'].split('/')[-1:])] = data[i]['text'] 

	print('Retrieved '+str(len(text_data))+' articles from wikiFile '+wikiDir+'/'+wikiFilePath)
	return text_data

def getWikiFile(wikiDir):
	for wikiFil in os.listdir(os.path.join(args['wiki_corpus_path'],wikiDir)):
		if not wikiFil.startswith('.'):
			#print(wikiDir, wikiFil)
			yield wikiFil

def fetchWikiText(article_title):
	for wikiDir in os.listdir(args['wiki_corpus_path']):
		if not wikiDir.startswith('.') and os.path.isdir(os.path.join(args['wiki_corpus_path'],wikiDir)):
			wikiFil = getWikiFile(wikiDir)
			#print(wikiFil)
			articleText = ''
			for wikiContainerFile in wikiFil: #get value yielded
				articleText = getArticleText2(article_title,wikiDir,wikiContainerFile)
				if len(articleText) > 0:
					print("Found "+article_title+' in '+wikiDir+'/'+wikiContainerFile)
					break;
			
			#if len(articleText) == 0:
			#	print(article_title+' not in '+wikiDir)
			#elif len(articleText) > 0:
			if len(articleText) > 0:
				return articleText

##for batch mode
def fetchWikiText2(article_titles,limit=581):
	articles = dict()
	for wikiDir in os.listdir(args['wiki_corpus_path']):
		if not wikiDir.startswith('.') and os.path.isdir(os.path.join(args['wiki_corpus_path'],wikiDir)):
			wikiFil = getWikiFile(wikiDir)
			#print(wikiFil)
			articleText = ''
			for wikiContainerFile in wikiFil: #get value yielded
				for article_title in article_titles:
					articleText = getArticleText2(article_title,wikiDir,wikiContainerFile)
					if len(articleText) > 0:
						print("Found "+article_title+' in '+wikiDir+'/'+wikiContainerFile)
						articles[article_title] = articleText
						articleText = ''
						if len(articles) == limit:
							return articles
			
				if len(articles) < len(article_titles):
					article_titles = [k for k in article_titles if k not in articles]#clean article titles already fetched.
				elif len(articles) >= len(article_titles):
					return articles



		



