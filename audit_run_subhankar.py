from reader import reader
from bert_semantic_audit import bert_similarity_score
import os
import sys
import nltk
from nltk import word_tokenize,sent_tokenize

import json
import pickle
import ast

import pyap

import pandas as pd
import regex as re

import json
import numpy as np

import pickle

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential,model_from_json

from sklearn.externals import joblib

import ftfy
from ftfy import fix_text


from nltk.corpus import stopwords
# import copy


from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
# from multiprocessing import Pool
# import multiprocessing

from pdf2image import convert_from_path
import pytesseract


from collections import defaultdict
# from gensim import corpora
# from gensim import models
# from gensim import similarities
from difflib import SequenceMatcher


lbl_sent = pd.DataFrame()
df_sen = pd.read_csv('/home/xelpmoc/Desktop/contracts/audit rights clause procurement - Sheet1.csv')

stemmer = SnowballStemmer(language='english')

STOPWORDS = set(stopwords.words('english'))

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_*]')
STOPWORDS = set(stopwords.words('english'))

# The maximum number of words to be used. (most frequent)
MAX_NB_WORDS = 50000
# Max number of words in each complaint.
MAX_SEQUENCE_LENGTH = 250
# This is fixed.
EMBEDDING_DIM = 100

stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}','’','=','#','$','&'])

# p = Pool(2)
# def extract(full_contract,param):
#     dates_ = []
#     durations_ = []
#     money_ = []
#     percent_=[]
#     act_ = []
#     place_ = []
#     numeric_= []
#     geo_place_ = []
#     address_= []
#     company_= []
#     contract_ = "".join(full_contract)
#     # print(bill_string)
#     contract_string = contract_.replace('\n', ' ')
#     contract_sent = sent_tokenize(contract_string)
    # print(contract_sent)
# nlp = spacy.load('en_core_web_lg')


def clean_text(text):
    """
        text: a string

        return: modified initial string
    """
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text. substitute the matched string in REPLACE_BY_SPACE_RE with space.
    text = BAD_SYMBOLS_RE.sub('', text) # remove symbols which are in BAD_SYMBOLS_RE from text. substitute the matched string in BAD_SYMBOLS_RE with nothing.
    text = text.replace('x', '')
#    text = re.sub(r'\W+', '', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # remove stopwors from text
    return text

def contract_extraction_function(name):
    cwd = os.getcwd()
    # new_cwd = (cwd+"/40-20200109T084836Z-001/40/")
    new_cwd = (cwd+"/40/")
    for foldername in os.listdir(new_cwd):
        contract_folder_name = new_cwd + foldername
        for filename in os.listdir(contract_folder_name):
            if filename == name:
                path = contract_folder_name + "/"+ name
                contract_name = contract_folder_name + "/" + filename
                for pdf_file in os.listdir(contract_name):
                    if pdf_file.endswith(".pdf"):
                        pdf_path = path + "/" + pdf_file

                        # pdf_path = '/home/xelpmoc/Documents/exigent-category-extraction-master/date contracts'+"/"+contract_name_+'/'+ pdf_file
                        return pdf_path



def all_contract_id():
    data = {}
    inst_list = []
    contract_list = []
    contract_id_list = []
    read_file = open("aug_data.json")
    data = json.load(read_file)
    result = data.get("result")
    contract_values = result.get("contactValues")
    for i in range(0,len(contract_values)):
        # random_contract_number = random.randint(0,len(contract_values)- 1)
        # random_contract = contract_values[random_contract_number]
        random_contract_id = contract_values[i]["contract_id"]
        random_contract_name = contract_values[i]["contract_name"]
        if random_contract_name not in contract_training_lst:
            contract_list.append(random_contract_name)
            contract_id_list.append(random_contract_id)
    return contract_id_list, contract_list

def ocr_reader(file_url):
	response_list = []
	print("Found file url {0}".format(file_url))
	try:
		pages = convert_from_path(file_url, grayscale=True)
		count = 0
		for page in pages:
			count = count + 1
			print("Converting page {0} of {1}".format(count,file_url))
			text = str(((pytesseract.image_to_string(page))))
			text = text.replace('-\n', '')
			response_list.append(text)
		return ''.join(response_list)
	except:
		return ''.join(response_list)




# df = pd.read_csv('places_training_set.csv')
# contract_training_lst = []
# [contract_training_lst.append(i) for i in df['contract_name']]


# contract_id_list , contract_name_list = all_contract_id()

# for nam in contract_name_list[1:2]
# contract_name_ = ['contract-1564158294589','contract-1564383595381','contract-1564383725278','contract-1564383738737','contract-1564383772362','contract-1564384383090','contract-1564384415750','contract-1564384515275','contract-1564384530177','contract-1564384821016','contract-1564384832570','contract-1564384845698','contract-1564384928276','contract-1564384947598','contract-1564385086777','contract-1564385098012',
# 'contract-1564385109231','contract-1564385118665','contract-1564452502149','contract-1564452556466','contract-1564570886872','contract-1564571940021','contract-1564573020447','contract-1564573038249','contract-1564719690419','contract-1564719709404','contract-1564725318623','contract-1564725997299','contract-1564726059298','contract-1564729198973','contract-1564725318623','contract-1564725997299','contract-1564726059298','contract-1564729241762','contract-1564730652569','contract-1564730686633','contract-1564941647467','contract-1565152848594','contract-1565153295150','contract-1564726085936','contract-1564729241762','']

# directory = os.getcwd()
#
# for r, d, f in os.walk(directory + '/contracts/'):
#     print(r,f)
#     # print(r)
#     # print(d)
#     if len(d) > 0:
# # #
# # #
#         for contract_name_ in d:
# #
#
#
#

# contract_string = ocr_reader('cbre/subhankarGermanySNAPCBRELocalAgrementexecuted.pdf')


# contract_name_ = "contract-1570769526433"
final_out = {"text":[], "Contracts":[]}
df = pd.read_csv('audit_clause_bert_corpus.csv')

# contract_nam = df["id"][173:len(df["instruction"])]
contract_nam = df["id"][0:172]
# contract_name_ = "contract-1570597538968"

#
#
for contract_name_ in contract_nam:
#
#
    contract_name_path = contract_extraction_function(contract_name_)
    if contract_name_path == None:
        # sys.exit('pdf not present')
        continue
    else:
        pass
    # place_ = []

    contract_string = reader(contract_name_path)
    contract_string = "".join(contract_string)

    contract_string = contract_string.replace('\n', ' ')
    # print(contract_string)
    contract_sentences = []
    contract_sent = sent_tokenize(contract_string)
    [contract_sentences.append(fix_text(s)) for s in contract_sent]
    # print(contract_sentences)

    #################################################
    # for val in contract_sentences:
    #
    #
    #     sent_ = re.sub("\\.+",' ',val)
    #     sent_1 = re.sub('_+', ' ', sent_)
    #     # sent_2 = re.sub('-+', ' ', sent_1)
    #     sent = re.sub(' +', ' ', sent_1)
    #     doc = nlp(sent)
    #     if sent.strip():
    #         for ent in doc.ents:
    #             if ent.label_ is 'GPE':
    #                 place_.append(sent)
    # places_sents_ls = list(set(place_))
    ##########################################################
    match_sentences = []

    # for v in places_sents_ls:
    for val in contract_sentences:

        sent = re.sub("\\.+",' ',val)
        sent = re.sub('_+', ' ', sent)
        sent = re.sub('-+', ' ', sent)
        v = re.sub(' +', ' ', sent)

        # Top 5 words in a list
        # my_condition_phrases = copy.deepcopy(final_lst)
        with open('frequency_audit.pkl', 'rb') as f:
            my_condition_phrases= pickle.load(f)
            my_condition_phrases = my_condition_phrases[1:len(my_condition_phrases)-1]
        temp_lst = []
        temp_stem = []
        word_lst = word_tokenize(v)
        [temp_lst.append(stemmer.stem(i)) for i in word_lst if i not in stop_words]
        matched_lst = list(set(temp_lst).intersection(my_condition_phrases))

        if len(matched_lst) > 0:
            match_sentences.append(v)
    contract_sentences.clear()
    similarity_lst = []
    # print(match_sentences)

    # data = ('\n\n').join(match_sentences)
    # print(data)
    for match_sent in match_sentences:
        score = bert_similarity_score(match_sent)
        similarity_lst.append({"phrase" : match_sent, "score": score})



    # final_output = []
    # print(similarity_lst)



    #sorting the sentences and getting top 5 for classification
    float_val = []
    for x in similarity_lst:
        for k,v in x.items():
            if isinstance(v, float):
                float_val.append(v)
    float_val.sort(reverse=True)
    lenght = len(float_val)
    i = 0
    top_score = []
    flag = 0
    while i < 5:
        try:

            highest_index = next((index for (index, d) in enumerate(similarity_lst) if d["score"] == float_val[i]), None)
            top_score.append(similarity_lst[highest_index])
            i += 1
        except:

            flag = 1

            break

    if flag == 1:


        top_score.clear()
        for j in range(len(similarity_lst)):
            highest_index = next((index for (index, d) in enumerate(similarity_lst) if d["score"] == float_val[j]), None)
            top_score.append(similarity_lst[highest_index])
    else:
        pass


    high_match = []
    for g in top_score:
        [high_match.append(v1) for k1,v1 in g.items() if k1 == 'phrase']

    sentnce = df_sen.loc[df_sen['id'] == contract_name_, 'instruction'].iloc[0]
    match_ratio = []
    for itr,item in enumerate(high_match):
        ratio = SequenceMatcher(None, item, sentnce).ratio()
        match_ratio.append(ratio)

    max_ratio = max(match_ratio)
    if max_ratio > 0.6:
        indx = match_ratio.index(max_ratio)
        temp2 = pd.DataFrame({'sentence': [high_match[indx]], 'contract_name': [contract_name_],
                              'label': ['1']})
        lbl_sent = pd.concat([lbl_sent, temp2])
        high_match.pop(indx)
        for sents in high_match:
            temp2 = pd.DataFrame({'sentence': [sents], 'contract_name': [contract_name_],
                                  'label': ['0']})
            lbl_sent = pd.concat([lbl_sent, temp2])
    else:
        temp2 = pd.DataFrame({'sentence': [sentnce], 'contract_name': [contract_name_],
                              'label': ['1']})
        lbl_sent = pd.concat([lbl_sent, temp2])

    lbl_sent = lbl_sent.reset_index(drop=True)

lbl_sent.to_csv('sentence_label.csv')
#     audit_sentences = ('\n\n').join(high_match)
#
#     final_out['text'].append(audit_sentences)
#     final_out['Contracts'].append(contract_name_)
#     print('this contract is done')
#
# pd.DataFrame(final_out).to_csv('clause_model/audit_rights_from_bert.csv', index = False)
# print('\n\n-------------------------------------Game Over-----------------------------------------\n\n')
