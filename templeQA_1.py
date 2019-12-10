#Uses transformers from https://huggingface.co/transformers/pretrained_models.html
import torch
import transformers
from transformers import BertForQuestionAnswering,BertTokenizer, BertConfig

from WikiProcessing import *
from WebProcessing import *
import re
from KGconfig import *


tokenizer = BertTokenizer.from_pretrained(args['bert_path'])
config_class = BertConfig.from_pretrained(args['bert_path'])
model = BertForQuestionAnswering.from_pretrained(args['bert_for_qa'])
'/Users/pradh4/Downloads/

def stringFix(st):
	if ' ##' in st:
		return st.replace(' ##','')

def getBertAnswer(question, text):
	global tokenizer, model
	input_text = "[CLS] " + question + " [SEP] " + text + " [SEP]"
	input_ids = tokenizer.encode(input_text)
	token_type_ids = [0 if i <= input_ids.index(102) else 1 for i in range(len(input_ids))]
	try:
		start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]))
		all_tokens = tokenizer.convert_ids_to_tokens(input_ids)
		ans = ' '.join(all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1])
		return (stringFix(ans))
	except:
		return None

def storeCorpus(templeCorpus):
	with open('data/WebTempleCorpus.json', 'w') as fp:
		json.dump(templeCorpus, fp)

#Add single temple QAs to temple Corpus dict in json
def storeCorpus1(templeCorpus):
	fp = open('data/WebTempleCorpus.json', 'r')
	QA = json.load(fp)
	fp.close()
	updateFlag = False
	for key in templeCorpus:
		if not key in QA:
			QA[key] = templeCorpus[key]
			updateFlag = True
	if updateFlag:
		storeCorpus(QA)

##extract QAs and store. Batch mode.
## Run only once
def extractQA():
	templeCorpus = dict()#dict of dictionaries (i.e. templData)
	Qs = ['Where is temple located?', 'Where is the temple situated?', 'The temple is dedicated to whom?', 'Who is the diety?','When was the temple built?','What are the darshan hours?','What is the average darshan duration?','What are the facilities available?','Who manages the temple?','What is the language?','What is contact email?','What is contact phone?','What is the website?']
	templeCorpus["head_line"] = {"questions":Qs}

	webFile = getWebFile()
	for webScrapFile in webFile: #get value yielded
		articleTitle = webScrapFile
		context = getWebText(webScrapFile)
		print(articleTitle)
		templeData = dict() #store data of one temple

		As = [[]] * len(Qs)
		templeData["context"] = context

		##Bert has limitation on the length of the input text as 512 tokens
		#Qs have max 6 and avg 4.6 tokens. Allocating 10 tokens for q
		#Answer has max 500 tokens
		limit = 250
		chunks = []
		if len(context.split()) > limit:
			for i in range(len(context.split())//limit):
				chunks.append(' '.join(context.split()[i*limit:(i+1)*limit]))
			chunks.append(' '.join(context.split()[len(context.split())//limit *limit :]))
		else:
			chunks.append(context)
		print([len(chunk.split()) for chunk in chunks])

		for ques in Qs: #questions:
			aa =[]
			for chunk in chunks:
				ans = getBertAnswer(ques,chunk)
				if ans != None:
					aa.append(ans)
				else:
					aa.append(' ')
			As[Qs.index(ques)] = aa
			print (' Q = '+ques)
			print(aa)
		c = []
		c.extend(As)
		print(c)
		templeData["answers"] = c
		templeCorpus[articleTitle] = templeData
		#print(templeCorpus[articleTitle])

		#if(len(templeCorpus)%3 == 0):
		storeCorpus(templeCorpus)

#extract QAs and stores. Single temple mode
def extractQA1(articleTitle):
	templeCorpus = dict()#dict of dictionaries (i.e. templData)
	Qs = ['Where is temple located?', 'Where is the temple situated?', 'The temple is dedicated to whom?', 'Who is the diety?','When was the temple built?','What are the darshan hours?','What is the average darshan duration?','What are the facilities available?','Who manages the temple?','What is the language?','What is contact email?','What is contact phone?','What is the website?']
	templeCorpus["head_line"] = {"questions":Qs}
	context = getWebText(articleTitle+'.txt')
	print(articleTitle)
	templeData = dict() #store data of one temple

	As = [[]] * len(Qs)
	templeData["context"] = context

	##Bert has limitation on the length of the input text as 512 tokens
	#Qs have max 6 and avg 4.6 tokens. Allocating 10 tokens for q
	#Answer has max 500 tokens
	limit = 250
	chunks = []
	if len(context.split()) > limit:
		for i in range(len(context.split())//limit):
			chunks.append(' '.join(context.split()[i*limit:(i+1)*limit]))
		chunks.append(' '.join(context.split()[len(context.split())//limit *limit :]))
	else:
		chunks.append(context)
	print([len(chunk.split()) for chunk in chunks])

	for ques in Qs: #questions:
		aa =[]
		for chunk in chunks:
			ans = getBertAnswer(ques,chunk)
			if ans != None:
				aa.append(ans)
			else:
				aa.append(' ')
		As[Qs.index(ques)] = aa
		print (' Q = '+ques)
		print(aa)
	c = []
	c.extend(As)
	print(c)
	templeData["answers"] = c
	templeCorpus[articleTitle] = templeData
	#print(templeCorpus[articleTitle])

	storeCorpus1(templeCorpus)
	return templeCorpus


def main():
	extractQA()

if __name__ == '__main__':
    main()
