# Improve Recall and Precision of Diety Extraction
# Pre-requisite : Run coreNLP client running in poot 9000

from stanza.server import StartServer
from stanza.server.client import CoreNLPClient
CORE_NLP_CLIENT = CoreNLPClient(server='http://localhost:9000', start_server=StartServer.DONT_START)

import json
import pandas as pd
import os
import pickle
import re
import numpy as np

from Questions import Questions

def load_TS_file(ts_file):
    f = open(ts_file)
    CtQtAt = json.load(f)
    f.close()
    return CtQtAt

def get_CQA(ts_file):
    CtQtAt = load_TS_file(ts_file)
    count = 0
    contexts = []
    questions = []
    answers = []

    for tKey in CtQtAt:
        if tKey == 'head_line':
            Questions = CtQtAt['head_line']['questions']
        else:
            Context = CtQtAt[tKey]['context']
            for aa in range(len(CtQtAt[tKey]['answers'])):
                for ans in CtQtAt[tKey]['answers'][aa]:
                    if ans != ' ':
                        contexts.append(Context)
                        questions.append(Questions[aa])
                        answers.append(ans)
                        count += 1

    df = pd.DataFrame({'Context': contexts, 'Question': questions, 'Answer': answers})
    #print('%s : \tTemples %d, \tContext %d, \tQuestions %d, \tAns %d, \tAvg.facts %.2f' %(ts_file, len(CtQtAt),len(contexts),len(questions),len(answers),len(answers)/(1.0*len(CtQtAt))))
    print('%s : \t %d, \t %d, \t %d, \t %d, \t %.2f' %(ts_file, len(CtQtAt),len(contexts),len(questions),len(answers),len(answers)/(1.0*len(CtQtAt))))
    #df.to_csv('data/ct_qt_data.csv', index=False)
    #print(ts_file, len(CtQtAt), df.shape[0])
    return

def get_statistics(ts_file):
    dietyList = []
    CtQtAt = load_TS_file(ts_file)
    count = 0
    domain = 'temple'
    global Questions 
    questions = Questions(domain)
    diety_fact_no = questions.temple_facts.index('Diety') +1

    for tKey in CtQtAt:
        if tKey == 'head_line':
            Questions = CtQtAt['head_line']['questions']
        else:
            Context = CtQtAt[tKey]['context']
            Diety_answers = CtQtAt[tKey]['answers'][diety_fact_no]
            for ans in Diety_answers:
                if ans != ' ' and len(ans.split())<10:
                    dietyList.append(ans)

    uniqueList = list(set(dietyList))
    print(uniqueList)
    print('%s : \t %d ' %('Unique dieties in KG', len(uniqueList)))
    return

def get_pos_pattern(temple_text):
    ner_results = annotate_text(temple_text)
    print(temple_text)
    for sentence in ner_results.sentence:
        for token in sentence.token:
            print ('%s - %s -- %s --- %s'%(token.word, token.pos, token.coarseNER, token.fineGrainedNER))
        #print(sentence.mentions)

def annotate_text(text):

    try:
        return CORE_NLP_CLIENT.annotate(text, annotators=['ssplit', 'tokenize', 'lemma', 'ner'])
    except Exception as ex:
        print(str(ex))
        return None

def main():
    '''
    ts_files =['../WebTempleCorpus_github.json','data/WebTempleCorpus.json','data/WebTempleCorpus0.json','data/TempleCorpusForVolunteer0.json','data/TempleCorpusForVolunteer1.json','data/WebTempleCorpus1.json','data/TempleCorpusForVolunteer2.json','data/WebTempleCorpus2.json','data/TempleCorpusForVolunteer3.json']
    #print('\t : \tTemples , \tContext , \tQuestions , \tAns , \tAvg.facts ')   
    #for ts_file in ts_files:
    #	get_CQA(ts_file)
    for i in range(len(ts_files)):
        get_fact_statistics(ts_files[i])
    '''
    ts_file = '../WebTempleCorpus_github.json'
    get_statistics(ts_file)
    
if __name__ == '__main__':
    main()