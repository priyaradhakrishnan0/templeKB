#from laptop only. Use python3
#Uses transformers from https://huggingface.co/transformers/pretrained_models.html
import torch
import transformers
from transformers import BertForQuestionAnswering,BertTokenizer, BertConfig

from WikiProcessing import *
from WebProcessing import *
from statistics import load_TS_file
from Questions import Questions
from DietyExtractor import DietyExtractor
from LanguageExtractor import LanguageExtractor

import re
import logging

bert_dir = '/home/priya/Desktop/Models/bert_uncased_L-24_H-1024_A-16_1' #'/Users/pradh4/Downloads/wwm_uncased_L-24_H-1024_A-16'
#tokenizer = BertTokenizer.from_pretrained(bert_dir)#'/home/priya/Desktop/Models/bert_uncased_L-24_H-1024_A-16_1') 
#note that bert_config.json is copied to config.json in /Users/pradh4/Downloads/wwm_uncased_L-24_H-1024_A-16
#config_class = BertConfig.from_pretrained(bert_dir)#'/Users/pradh4/Downloads/wwm_uncased_L-24_H-1024_A-16')
model = BertForQuestionAnswering.from_pretrained('/home/priya/Desktop/Models/bertQA') #/Users/pradh4/Downloads/bert-large-uncased-whole-word-masking-finetuned-squad-pytorch_model.bin'
tokenizer = BertTokenizer.from_pretrained('/home/priya/Desktop/Models/bertQA')
Qs_museums = ['When was the museum established?','What are the opening days of the museum?','What are the visiting hours?','What is the entry fee?','What is the average tour duration?','What are the facilities available?','Who manages the museum?','Is docent guide available?','What is the language?','What is contact email?','What is contact phone?','Which is the website?']
Qs_temples = ['Where is temple located?', 'Where is the temple situated?', 'The temple is dedicated to whom?', 'Who is the diety?','When was the temple built?','What are the darshan hours?','What is the average darshan duration?','What are the facilities available?','Who manages the temple?','What is the language?','What is contact email?','What is contact phone?','What is the website?']
Qs_loc = ['Where is temple located?', 'Where is the temple situated?', 'Where does this temple exist?']# 1 #
Qs_diety = ['The temple is dedicated to whom?', 'Who is the diety?', 'Which god lives here?'] # 2 #
Qs_age = ['When was the temple built?', 'Which period does the temple belong?'] #'Whatat is the age of the building?'] # 3 #
#Festival info #Puja timing, Darshan hours Qs_timing 
Qs_festival = ['What are the visiting hours?', 'When is the temple open?', 'What is the timings?' ] # 4 #
#Prominent people associated with the temple
Qs_people = ['Who built the temple?'] # 5 #
#trivia, Legend
Qs_trivia = ['What is the legend?'] # 6 #
Qs_manage = ['Who manages the temple?', 'Who overlooks temple administration?'] # 7 #
Qs_language = ['What is the language?'] # 8 #
Qs_address = ['What is the email?','What is the mobile or phone number?','Is there a website?','Whom to contact for more information?'] # 9 #

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
	#with open('data/WebMuseumCorpus.json', 'w') as fp:
		json.dump(templeCorpus, fp)

def storeCorpus_improved(templeCorpus):
	with open('data/WebTempleCorpus_improved.json', 'w') as fp:
	#with open('data/WebMuseumCorpus.json', 'w') as fp:
		json.dump(templeCorpus, fp)

#Add single temple QAs to temple Corpus dict in json
def storeCorpus1(templeCorpus):
	fp = open('data/WebTempleCorpus.json', 'r')
	#fp = open('data/WebMuseumCorpus.json', 'r')
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
	#Qs = ['Where is temple located?', 'Where is the temple situated?', 'The temple is dedicated to whom?', 'Who is the diety?','When was the temple built?','What are the darshan hours?','What is the average darshan duration?','What are the facilities available?','Who manages the temple?','What is the language?','What is contact email?','What is contact phone?','What is the website?']
	Qs = Qs_temples 
	templeCorpus["head_line"] = {"questions":Qs}
	#templeData = dict() #store data of one temple
	#articleTitle = 'Thiruvananthapuram Sree Padmanabhaswamy Temple.txt'#'Dakshina Kailasam Thrissivaperoor Sree Vadakkunnatha Temple'
	#context = "This is the first Shiva temple created by Lord Parasurama. Shiva here is more popularly known as Vadakkunnathan. Vadakkunnatha Temple is situated at the heart of Thrissur city. The name Thrissur is derived from 'Thiru-Shiva-Peroor', which literally translates to 'The city of the sacred Shiva'. Thrissur was also known as Vrishabhadripuram, Vrishachala and Thenkailasam or Dakshina Kailasam(Kailasa of the south) in ancient days."
	#	fp.close()

	webFile = getWebFile()
	for webScrapFile in webFile: #get value yielded
		articleTitle = webScrapFile	
		context = getWebText(webScrapFile)
		#print(context)
		#print(articleTitle)
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

		#if(len(templeCorpus)%1 == 0):
		storeCorpus(templeCorpus)
		#break

#extract QAs and stores. Single temple mode
def extractQA1(articleTitle):
	templeCorpus = dict()#dict of dictionaries (i.e. templData)
	#Qs = ['When was the museum established?','What are the opening days of the museum?','What are the visiting hours?','What is the entry fee?','What is the average tour duration?','What are the facilities available?','Who manages the museum?','Is docent guide available?','What is the language?','What is contact email?','What is contact phone?','Which is the website?']
	#Qs = ['Where is temple located?', 'Where is the temple situated?', 'The temple is dedicated to whom?', 'Who is the diety?','When was the temple built?','What are the darshan hours?','What is the average darshan duration?','What are the facilities available?','Who manages the temple?','What is the language?','What is contact email?','What is contact phone?','What is the website?']
	Qs = Qs_museums
	templeCorpus["head_line"] = {"questions":Qs}
	#templeData = dict() #store data of one temple
	#articleTitle = 'Thiruvananthapuram Sree Padmanabhaswamy Temple.txt'#'Dakshina Kailasam Thrissivaperoor Sree Vadakkunnatha Temple'
	#context = "This is the first Shiva temple created by Lord Parasurama. Shiva here is more popularly known as Vadakkunnathan. Vadakkunnatha Temple is situated at the heart of Thrissur city. The name Thrissur is derived from 'Thiru-Shiva-Peroor', which literally translates to 'The city of the sacred Shiva'. Thrissur was also known as Vrishabhadripuram, Vrishachala and Thenkailasam or Dakshina Kailasam(Kailasa of the south) in ancient days."

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

	#storeCorpus1(templeCorpus)
	storeCorpus(templeCorpus)
	return templeCorpus

def runBert():
	question = Qs_temples[1]
	text = '''Tiru Agathiyan Palli Agastheeswarar -. Temple  - Shivastalam
    may be reproduced or used in any form without permission.
        is known primarily for its temple to Tyagarajar (one of the 7 Saptavitanka Stalams).
        Agastyampalli (Agathiyaanpalli) is a Shivastalam  located adjacent to the salt pans
        of Vedaranyam. This shrine is regarded as the 126th in the series
          of Tevara Stalams in the Chola Region south of the river Kaveri.Legend has it that Agastyar witnessed the divine
        marriage of Shiva and Parvati here. Interestingly, the same legend is associated with the
        Tyagarajar temple at Vedaranyam where a panel depicting the divine marriage is seen behind
        the Shivalingam in the sanctum. It is believed that Agasthyar built his hermitage here,
        and trekked up to Vedaranyam each day. Shiva here, is also known as Agnipureeswarar.
          Shiva's shrine faces the East while the Ambalshrine faces west. 
History: There are inscriptions here relating to Kulasekhara Pandyan
        (13th Cent AD)  and to the period of the Imperial Cholas. The image shown above is
        that of Tyagaraja at Tiruvarur, which is one of
[Abodes of Shiva - Home] [The Templenet Encyclopedia][Temple Architecture][Travel &'''
	#'Agastyampalli (Agathiyaanpalli) is a Shivastalam  located adjacent to the salt pans of Vedaranyam.'
	ans = getBertAnswer(question, text)
	print (' Q : '+question + ' A : '+ans)

def improve():
	templeCorpus = dict()#dict of dictionaries (i.e. templData)
	#Qs = Qs_loc+Qs_diety+Qs_age+Qs_festival+Qs_people+Qs_trivia+Qs_manage+Qs_language+Qs_address # # # # # 
	domain = 'temple'
	questions = Questions(domain)
	Qs = questions.fetchQs()
	templeCorpus["head_line"] = {"questions":Qs}

	webFile = getWebFile()
	for webScrapFile in webFile: #get value yielded
		articleTitle = webScrapFile	
		context = getWebText(webScrapFile)
		logging.info(context)
		#print(articleTitle)
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
		#logging.info([len(chunk.split()) for chunk in chunks])
		uniqueAns = [] 
		for ques in Qs: #questions:
			aa = []
			for chunk in chunks:
				ans = getBertAnswer(ques,chunk)
				if ans != None:
					ans = cleanAns(ques,ans)
					if ans not in uniqueAns:	
						aa.append(ans)
						uniqueAns.append(ans)
					else:
						aa.append(' ')
				else:
					aa.append(' ')
			As[Qs.index(ques)] = aa
			#logging.info(' Q = '+ques)
			#logging.info(aa)
		c = []
		c.extend(As)
		logging.info(c)
		#logging.info(uniqueAns)
		templeData["answers"] = c
		templeCorpus[articleTitle] = templeData
		#print(templeCorpus[articleTitle])

		#if(len(templeCorpus)%100 == 0):
		storeCorpus(templeCorpus)
		#	break

def improveRecall(ts_file):
	##Call improve() first
    CtQtAt = load_TS_file(ts_file)
    print('Prior to improving : \t %s \t %d' %( ts_file, len(CtQtAt)))
    count = 0
    question_to_fact_mapping = [[0,1,2],[3,4,5],[6,7],[8,9,10],[11],[12],[13,14],[15],[16,17,18, 19]] ##temple-improved
    #question_to_fact_mapping = [[0,1],[2,3],[4],[5],[6],[7],[8],[9],[10,11,12]] ##temple
    #question_to_fact_mapping = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9,10,11]] ##Museum

    domain = 'temple'
    global Questions 
    questions = Questions(domain)
    dietyExt = DietyExtractor()
    dietyList = dietyExt.get_dietyList()
    #diety_fact_no = questions.temple_facts.index('Diety') +1
    lngExt = LanguageExtractor()
    languageList = lngExt.getLanguageList()
    
    facts = [0] * len(question_to_fact_mapping)
    for tKey in CtQtAt:
        if tKey == 'head_line':
            Questions = CtQtAt['head_line']['questions']
        else:
            Context = CtQtAt[tKey]['context']
            
            for aa in range(len(CtQtAt[tKey]['answers'])):
                fact_no = [k for k in range(len(question_to_fact_mapping)) if aa in question_to_fact_mapping[k]][0]
                #print(fact_no, aa)
                vacant = True #
                for ans in CtQtAt[tKey]['answers'][aa]:
                    if ans != ' ':          
                        count += 1
                        vacant = False
 
                if vacant: #no ans for given question
                    temple_fact_name = questions.temple_facts[fact_no]
                    if temple_fact_name == 'Diety':
                        for word in Context.split():
                            if word in dietyList:
                                CtQtAt[tKey]['answers'][aa][0] = word
                                vacant = False
                                break
                    elif temple_fact_name == 'Language':
                        for word in Context.split():
                            if word in languageList:
                                CtQtAt[tKey]['answers'][aa][0] = word
                                vacant = False
                                break

    storeCorpus_improved(CtQtAt)            
    print('Stored improved Recall.') 
    	#Location , Diety, Age, Festival, Key-people, Trivia, Manage, Language, Address')
    print('data/WebTempleCorpus_improved.json : \t %d \t %d' %( count, len(CtQtAt)))
    return

def cleanAns(question, answer):
	answer = re.sub(r'\[CLS\].*\[SEP\]',' ',answer)
	return answer

def main():
	#logging.basicConfig(filename='./logs/templeQA_1.log', level=logging.DEBUG)
	
	#extractQA()
	#articleTitle = 'Vikram Pendse Cycles – A Journey into the past!'
	#extractQA1(articleTitle)
	#runBert() 
	#improve()
	ts_file = '../WebTempleCorpus_github.json'
	improveRecall(ts_file)

	###Trivia or Interesting facts : When the answer extracted is more than two sentences in length, it is an interesting fact.

if __name__ == '__main__':
    main()
