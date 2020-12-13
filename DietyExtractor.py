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

class DietyExtractor(object):


    def __init__(self):
        self.ts_file = '../WebTempleCorpus_github.json'

    def load_TS_file(self, ts_file):
        f = open(ts_file)
        CtQtAt = json.load(f)
        f.close()
        return CtQtAt

    def get_dietyList(self):
        dietyList = []
        dietyList_2 = []
        CtQtAt = self.load_TS_file(self.ts_file)
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
        #print('%s : \t %d ' %('Unique dieties in KG', len(uniqueList)))    
        #print(uniqueList)
        #Cleaning the entries
        stop_words_diety_name_pre = ['goddess', 'sri', 'lord', 'sree', 'shri']
        stop_words_diety_name_post = ['swami', 'devi']
        for name in uniqueList:
            name_tokens = name.split()
            if len(name_tokens) > 1:
                name_tokens = [i for i in name_tokens[:-1]  if i not in stop_words_diety_name_pre]
            dietyList_2.extend(' '.join(name_tokens))
        print('%s : \t %d ' %('Unique dieties in KG', len(uniqueList)))
        return dietyList_2

def main():
    '''
    ts_files =['../WebTempleCorpus_github.json','data/WebTempleCorpus.json','data/WebTempleCorpus0.json','data/TempleCorpusForVolunteer0.json','data/TempleCorpusForVolunteer1.json','data/WebTempleCorpus1.json','data/TempleCorpusForVolunteer2.json','data/WebTempleCorpus2.json','data/TempleCorpusForVolunteer3.json']
    #print('\t : \tTemples , \tContext , \tQuestions , \tAns , \tAvg.facts ')   
    #for ts_file in ts_files:
    #	get_CQA(ts_file)
    for i in range(len(ts_files)): if ans != ' ' and len(ans.split())<10:
        get_fact_statistics(ts_files[i])
    '''
    dietyExt = DietyExtractor()
    #ts_file = '../WebTempleCorpus_github.json'
    dietyExt.get_dietyList()
    
if __name__ == '__main__':
    main()