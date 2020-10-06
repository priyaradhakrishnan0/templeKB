# temple DS statistics

import json
import pandas as pd
import os
import pickle
import re
import numpy as np

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

def get_fact_statistics(ts_file):
    CtQtAt = load_TS_file(ts_file)
    count = 0
    question_to_fact_mapping = [[0,1],[2,3],[4],[5],[6],[7],[8],[9],[10,11,12]] ##temple
    #question_to_fact_mapping = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9,10,11]] ##Museum
    facts = [0] * len(question_to_fact_mapping)
    for tKey in CtQtAt:
        if tKey == 'head_line':
            Questions = CtQtAt['head_line']['questions']
        else:
            Context = CtQtAt[tKey]['context']
            for aa in range(len(CtQtAt[tKey]['answers'])):
                for ans in CtQtAt[tKey]['answers'][aa]:
                    if ans != ' ':
                        fact_no = [k for k in range(len(question_to_fact_mapping)) if aa in question_to_fact_mapping[k]][0]
                        #print(fact_no)
                        facts[fact_no] = facts[fact_no] + 1    
                        count += 1

    print('%s : \t %d \t %d' %(ts_file, count, len(CtQtAt)))
    print(facts)
    print([facts[k]/(len(CtQtAt)*1.0) for k in range(len(facts))])
    return

def main():
    ts_files =['../WebTempleCorpus_github.json','data/WebTempleCorpus.json','data/WebTempleCorpus0.json','data/TempleCorpusForVolunteer0.json','data/TempleCorpusForVolunteer1.json','data/WebTempleCorpus1.json','data/TempleCorpusForVolunteer2.json','data/WebTempleCorpus2.json','data/TempleCorpusForVolunteer3.json']
    #print('\t : \tTemples , \tContext , \tQuestions , \tAns , \tAvg.facts ')   
    #for ts_file in ts_files:
    #	get_CQA(ts_file)
    for i in range(len(ts_files)):
        get_fact_statistics(ts_files[i])
    '''
    ts_file = 'data/WebMuseumCorpus.json'
    get_fact_statistics(ts_file)
    '''
if __name__ == '__main__':
    main()