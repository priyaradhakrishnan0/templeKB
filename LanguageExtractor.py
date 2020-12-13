# Improve Recall and Precision of Diety Extraction
# 09 Dec 2020
#Priya R

import json
import pandas as pd
import os
import pickle
import re
import numpy as np
from os import listdir
from os.path import isfile, join
import xlrd

from Questions import Questions

#Language list from https://en.wikipedia.org/wiki/List_of_languages_by_number_of_native_speakers_in_India

class LanguageExtractor(object):


    def __init__(self):
        self.ts_file = '../WebTempleCorpus_github.json'

    def load_TS_file(self, ts_file):
        f = open(ts_file)
        CtQtAt = json.load(f)
        f.close()
        return CtQtAt

    def get_language_statistics(self, ts_file):
        languages = getLanguageList()
        dietyList = []
        CtQtAt = load_TS_file(ts_file)
        count = 0
        domain = 'temple'
        global Questions
        questions = Questions(domain)
        lang_fact_no = questions.temple_facts.index('Language')
        Qs = questions.fetchQs()
        for q in questions.temple_fact_mapping[lang_fact_no]:
            print(Qs[q])

        for tKey in CtQtAt:
            if tKey == 'head_line':
                Questions = CtQtAt['head_line']['questions']
            else:
                Context = CtQtAt[tKey]['context']
                lang_ans = ''
                for word in Context.split():
                    if word in languages:
                        lang_ans = word
                        print(tKey, lang_ans)
                        dietyList.append((tKey, lang_ans))
                        pass

        print('Lang for %d KG'%len(dietyList))
        return

    def getLanguageList(self):
        wiki_lang_list = '../templeKB_2.xlsx'
        lines = []
        workbook = xlrd.open_workbook(os.path.join(wiki_lang_list))
        lang_sheet = workbook.sheet_by_name('Language List')
        for row_idx in range(1, lang_sheet.nrows):
            lang_line = lang_sheet.cell(row_idx, 1)
            if lang_line not in lines:
                lines.append(lang_line.value.lower())
        print('Read %d lines of lang from %s'%(len(lines), wiki_lang_list))
        #print(lines)
        return lines

def main():
    #ts_file = '../WebTempleCorpus.json'
    #get_language_statistics(ts_file)
    langExt = LanguageExtractor()
    langExt.getLanguageList()

if __name__ == '__main__':
    main()
