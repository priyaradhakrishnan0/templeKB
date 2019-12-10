#Create KB facts on temples from a webpage on temples
import numpy as np
import pickle
import json
import csv
 
from KGconfig import *
from Scrapper import scrape
from templeQA_1 import *
from preprocess_modules import get_temple_dataset1, tokenize_and_convert, tokenize_and_convert_qa, load_TS_file, get_unanswered
from train_cq import predict_model as predict_cq
from train_qa import predict_model as predict_qa


embedding_matrix = np.load('data/embedding_matrix.npy')
##Scrape the URL and create templeName.txt and update metadata
def single():
    print(args['url'])
    #templeFileName = scrape(args['url'])
    templeFileName = 'Tiruchendur Senthilaandavar Temple.txt'#'Vatapi Ganapati.txt' #'Karpaka Vinayakar Temple Pillayarpatti.txt'
    articleTitle = templeFileName.replace('.txt','')

    ##Create QA pairs and store
    templeCorpus = extractQA1(articleTitle)

    ##Correct the QA pairs
    temple_cq, temple_qa = get_temple_dataset1(templeCorpus)
    word2ix = pickle.load(open('data/word2ix.pkl', 'rb')) # <= ensure this has widest vocab
    temple_xq, temple_xc = tokenize_and_convert('temple', temple_cq, word2ix, 10, 255, 'test/')
    print("temple_xq shape "+str(temple_xq.shape))
    print("temple_xc shape "+str(temple_xc.shape))
    preds = predict_cq(temple_xq, temple_xc)

    print(preds.shape)
    for i,x in enumerate(preds):
        if (x[0] >= 0.5):
            print('RIGHT : '+str(temple_cq[i,1:]))
        else:
            print('WRONG : '+str(temple_cq[i,1:]))

    temple_qa = np.asarray([x for i,x in enumerate(temple_qa) if "[CLS] " not in temple_qa[i,2] and "[SEP]" not in temple_qa[i,2]])
    print("temple_qa after cleaning = "+str(temple_qa.shape[0]))
    temple_xa, temple_xcq = tokenize_and_convert_qa('temple', temple_qa, word2ix, 10, 255, 'test/')
    print("temple_xa shape "+str(temple_xa.shape))
    print("temple_xcq shape "+str(temple_xcq.shape)) 
    #print("Embedding Matrix shape "+str(embedding_matrix.shape))
    preds = predict_qa(temple_xa, temple_xcq)

    print(preds.shape)
    for i,x in enumerate(preds):
        if (x[0] >= 0.5):
            print('RIGHT : '+str(temple_qa[i,1:]))
        else:
            print('WRONG : '+str(temple_qa[i,1:]))

#create QA from wiki for volunteers to edit
def createVolunteerInput():
    CtQtAt = dict()
    ts_file ='data/TempleCorpusForVolunteer2.json'
    CtQtAt = load_TS_file(ts_file)
    Questions = CtQtAt['head_line']['questions']
    unQ = get_unanswered(CtQtAt)
    
    ##Correct the QA pairs
    temple_cq, temple_qa = get_temple_dataset1(CtQtAt)
    word2ix = pickle.load(open('data/word2ix.pkl', 'rb')) # <= ensure this has widest vocab
    temple_xq, temple_xc = tokenize_and_convert('temple', temple_cq, word2ix, 10, 255, 'test/')
    print("temple_xq shape "+str(temple_xq.shape))
    print("temple_xc shape "+str(temple_xc.shape))
    preds_cq = predict_cq(temple_xq, temple_xc)
    print(preds_cq.shape)

    #temple_qa = np.asarray([x for i,x in enumerate(temple_qa) if "[CLS] " not in temple_qa[i,2] and "[SEP]" not in temple_qa[i,2]])
    #print("temple_qa after cleaning = "+str(temple_qa.shape[0]))
    temple_xa, temple_xcq = tokenize_and_convert_qa('temple', temple_qa, word2ix, 10, 255, 'test/')
    print("temple_xa shape "+str(temple_xa.shape))
    print("temple_xcq shape "+str(temple_xcq.shape)) 
    #print("Embedding Matrix shape "+str(embedding_matrix.shape))
    preds_qa = predict_qa(temple_xa, temple_xcq)
    print(preds_qa.shape)

    with open(ts_file.replace('.json','.csv'), 'w') as volunteerFile:
        csvwriter = csv.writer(volunteerFile, delimiter='\t') 
        count = 0
        prev_context = temple_cq[0,0] #initializing to first context
        for i,x in enumerate(temple_cq):
            if temple_cq[i,0] != prev_context:
                #next temple. 
                #print unanswered Qs of previous temple
                for q in unQ[count]:
                    rowDict = dict()
                    rowDict['context'] = prev_context
                    rowDict['question'] = q
                    rowDict['answer'] =  ' '
                    rowDict['C/Q'] = 'NONE'
                    rowDict['Q/A'] = 'NONE'
                    csvwriter.writerow(list(rowDict.values()))              
                prev_context = temple_cq[i,0] 
                count += 1

            rowDict = dict()
            rowDict['context'] = temple_cq[i,0]
            rowDict['question'] = temple_cq[i,1]
            rowDict['answer'] = temple_qa[i,2]
            #rowDict['decision'] = ' '
            if (preds_cq[i,0] >= 0.5):
                rowDict['C/Q'] = 'RIGHT'
            else:
                rowDict['C/Q'] = 'WRONG'
            if (preds_qa[i,0] >= 0.5):
                rowDict['Q/A'] = 'RIGHT'
            else:
                rowDict['Q/A'] = 'WRONG'
            csvwriter.writerow(list(rowDict.values()))
            #print(rowDict.values())

    
def main():
    #single()
    #createVolunteerInput()


if __name__ == '__main__':
    main()
