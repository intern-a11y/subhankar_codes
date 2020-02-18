import pdftotext
import os
import glob
import weakref
import re
import itertools
from collections import Counter
import pprint
import fitz
import PyPDF2
import time

import json
import string
#from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize
#from nltk.stem import WordNetLemmatizer,PorterStemmer


# current_dir=os.getcwd()


class ContractStructure(object):
	def __init__(self,filename,headings=None,):
		self.filename = filename
		self.headings = headings
		self.lastHeading = None

# 	def printClass(self):
# 		print ("------------\n")
# 		print ("Filename "+self.filename + "\n")
# 		for k,v in self.headings.items():
# 			print (k + "\n" + v)

# def getProgressiveHeaders(clause,convert_contract):
# 	subclause = []
# 	match_indicator = 0
# 	ASCII_a = 97
# 	ASCII_A = 65
# 	#remove multiple spaces if there are any
# 	clause = ' '.join(clause.split())
# 	alpha_prog = "\([^)(\d)]\)"
# 	alpha_prog_find = re.findall(alpha_prog,clause)
# 	#check for progression consistency
# 	for idx,value in enumerate(alpha_prog_find):
# 		local_value = value
# 		local_value = local_value.replace('(','').replace(')','')
# 		if ord(local_value) == (ASCII_a + idx):
# 			print ("Found " + "("+value+")" + " in progression")
# 		else:
# 			print(value + " was not in progression - removing")
# 			alpha_prog_find.remove(value)


# 	no_progressions = len(alpha_prog_find)
# 	while match_indicator < no_progressions-1:

# 		subclause.append(clause[clause.find(alpha_prog_find[match_indicator]):clause.find(alpha_prog_find[match_indicator+1])])
# 		match_indicator = match_indicator + 1
# #		print (matches)
# 	convert_contract.progressiveHeadings = subclause
# 	return convert_contract.progressiveHeadings


# def calculate_health(pdfPath):
# 	#Idea : Predict images in the pdf in percent to page
# 	#Params : pdf path
# 	#return : percent of images in pdf
# 	#return type : int

# 	doc = fitz.open(pdfPath)
# 	number = 0
# 	for i in range(len(doc)):
# 			if(doc.getPageImageList(i)):
# 					number += 1
# 	percent = (len(doc) - number) / len(doc) * 100
# 	return percent

# def key_limit(json_data,key_name,limit=5):
# 	#Idea : get list of instruction for given key
# 	#Params : json data, key_name, limit
# 	#return : dict with key_name as key and list of instruction
# 	#return type : dict
# 	new_json[key_name]=[]
# 	limit_count=0
# 	for results in json_data['result']:
# 		for heading,head_key in results['keyValues']['datamodel_structure'][0].items():
# 				for key_values, values in head_key.items():
# 					if "instruction" in values and key_values==key_name and limit_count<limit and values["instruction"] not in [None,""]:
# 							new_json[key_name].append(values["instruction"])
# 							limit_count+=1
# 	return new_json


# def lemm_word_count (json_data):
# 	#Idea : get json with lemm word frequency in the datamodal instruction
# 	#Params : json data
# 	#return : json data key_values as keys and frequency of words as nested dict
# 	#return type : json

# 	new_json={}
# 	punctuation_string= string.punctuation+"“”’``||''"

# 	# nltk objects
# 	lemmatizer = WordNetLemmatizer()
# 	stop_words = set(stopwords.words('english'))

# 	for results in json_data['result']:
# 		for heading,head_key in results['keyValues']['datamodel_structure'][0].items():
# 			for key_values, values in head_key.items():
# 				if "instruction" in values and values["instruction"] not in ["",None] :
# 					if key_values not in new_json:
# 						new_json[key_values]={} #added key to json
# 					word_list=word_tokenize(values["instruction"])
# 					lemmatizer_list=[lemmatizer.lemmatize(word) for word in word_list if not word in punctuation_string]
# 					stopWord_free_list=[lemmat_word for lemmat_word in lemmatizer_list if not lemmat_word in stop_words]
# 					for instruction_word in stopWord_free_list:
# 						if instruction_word not in new_json[key_values]:
# 						#if not new_json[key_values].get(instruction_word, None)
# 							new_json[key_values][instruction_word]=1
# 						elif instruction_word in new_json[key_values]:
# 							new_json[key_values][instruction_word]+=1
# 	return(new_json)


# def stem_word_count (json_data):
# 	#Idea : get json with setmed word frequency in the datamodal instruction
# 	#Params : json data
# 	#return : json data key_values as keys and frequency of words as nested dict
# 	#return type : json

# 	new_json={}
# 	punctuation_string= string.punctuation+"“”’``||''"

# 	# nltk objects
# 	steming = PorterStemmer()
# 	stop_words = set(stopwords.words('english'))

# 	for results in json_data['result']:
# 		for heading,head_key in results['keyValues']['datamodel_structure'][0].items():
# 			for key_values, values in head_key.items():
# 				if "instruction" in values and values["instruction"] not in ["",None] :
# 					if key_values not in new_json:
# 						new_json[key_values]={} #added key to json
# 					word_list=word_tokenize(values["instruction"])
# 					lemmatizer_list=[steming.stem(word) for word in word_list if not word in punctuation_string]
# 					stopWord_free_list=[lemmat_word for lemmat_word in lemmatizer_list if not lemmat_word in stop_words]
# 					for instruction_word in stopWord_free_list:
# 						if instruction_word not in new_json[key_values]:
# 						#if not new_json[key_values].get(instruction_word, None)
# 							new_json[key_values][instruction_word]=1
# 						elif instruction_word in new_json[key_values]:
# 							new_json[key_values][instruction_word]+=1
# 	return(new_json)


# def image_page_list(pdfPath):
# 	#Idea : to get all the pages with images
# 	#Params : path to pdf file
# 	#return : list it's page numbers


# 	doc = fitz.open(pdfPath)
# 	image_list=[]
# 	for i in range(len(doc)):
# 		if(doc.getPageImageList(i)):
# 			image_list.append(i)
# 	return image_list

def collectHeadings(converted_pdf):
	#function params : converted_pages : Appended string that has the entire contract (post PdftoText)
	#functionality : any improvements for collecting Headings
	#returns : dict (struct) key,value = heading, content
	# 	{
	# 		heading1 : content1,
	# 		headingn :  contentn,
	# }
	# heading : str, content : str

	#fixme : refer output of printclass() : every line is breaking in values in  variable dictonary
# ==================================New heading code ========================================
	# print(converted_pdf)

	# regex = r"^\s*?(([a-z]{,2}|[0-9]{,2})\s*\.)?(\s*([A-Z]){2,}(\s|,|;)*)+"
	regex = r"^\s*?(([\w\d]{,2})\s*\.)?(\s*([A-Z]){2,}(\s|,|;)*)+"   #improved regex, if this fails comment this and comment previous regex
	all_cap= r'(([A-Z]+(\s|,|;)*)+[A-Z]+)'
	matches = re.finditer(regex, converted_pdf, re.MULTILINE)

	heading_index = {}
	list_heading = {}
	for matchNum, match in enumerate(matches, start=1):
		if match.group():
			heading_index[str(match.start())] = {
				"end": match.end(), "heading": match.group().strip()}



	heading_start_list = list(heading_index.keys())
	heading_context_dict = dict()

	for i in range(len(heading_start_list)):
		# print(len(heading_start_list))
		heading_dict = heading_index[heading_start_list[i]]

		heading = heading_dict['heading']

		# if i != len(heading_start_list)-1:
		#     print(final_pdf[heading_dict['end']+1:int(heading_start_list[i+1])])
		if i != len(heading_start_list)-1:
			context = converted_pdf[heading_dict['end']+1:int(heading_start_list[i+1])]
			# print(context)
			heading_context_dict[heading] = context
		else:
			context = converted_pdf[heading_dict['end']+1:]
			heading_context_dict[heading] = context
	return heading_context_dict

# ==========================================================================
	# Nihal Code returns dict of headings and there contants
	# needs improvement with regex
	# @todo Nihal function
	#important Dont remove RegExTest.txt

# ++++++++++++++++++++++code to be uncomment if previous line code doesn't work  ++++++++++++++++++++++++++++++++



	# with open(current_dir+'/extraction/RegExtest.txt','w') as text_file:
	# 	text_file.write(converted_pdf)
	# text_file.close()

	# file_data = open(current_dir+'/extraction/RegExtest.txt', 'r')
	# data = file_data.readlines()
	# file_data.close()

	# all_cap = r'(\s[A-Z]+\s*?)+'

	# reg4 = r'^.?\s*?(([A-Z]{,2}|[0-9]{,2})\s*\.)(\s*(([A-Z]|[0-9]){2,}|A)(\s|,|;)*)+'
	# reg5 = r'^\s*?(([a-z]{,2}|[0-9]{,2})\s*\.)(\s*([A-Z]){2,}(\s|,|;)*)+'
	# heading=''
	# list_heading = {}
	# for line in data:

	# 	if(re.search(reg5,line)):
	# 		# print(re.search(all_cap,re.search(reg5,line).group(0)).group(0).strip())
	# 		heading=re.search(all_cap,re.search(reg5,line).group(0)).group(0).strip()
	# 		if len(heading)>0 and heading not in list_heading:
	# 			list_heading[heading] = ''
	# 	if heading in list_heading:
	# 		list_heading[heading]=list_heading[heading] +" "+line
	# return (list_heading)




	# headings = []
	# l1 = []
	# for current_word in converted_pages.split("\n"):
	# 	if current_word.isupper():
	# 		headings.append(current_word)
	# 	else:
	# 		l1 = current_word.split('.')
	# 		if((len(l1)>1 and l1[1].isupper())):
	# 			headings.append(l1[1])
	# pattern_head = []
	# for heading in headings:
	# 	pattern_head.append(re.sub(r'\s+',' ',heading).strip())
	# pattern_head2 = []
	# for i in range(len(pattern_head)):
	# 	pattern_head2.append(re.sub(r'[^A-Z a-z]',' ',pattern_head[i]).strip())

	# c = Counter(pattern_head2)
	# pattern_head3=[k for k,v in c.items() if v == 1]

	# pattern_head4=[]
	# for words in pattern_head3:
	# 	if len(words)>=3:
	# 		words = words.strip()
	# 		pattern_head4.append(words.lstrip())

	# dictionary={}
	# key=-1
	# clause=''
	# for sentence in converted_pages.split("\n"):
	# 	t = sentence
	# 	temp = ""
	# 	next_sent=""
	# 	if t.isupper():
	# 		temp=re.sub('\s+', ' ', t).strip()
	# 		temp = re.sub(r'[^A-Z a-z]', '', temp)
	# 		temp = temp.strip()
	# 	else:
	# 		temp1=sentence.split('.')
	# 		if((len(temp1)>1) and temp1[1].isupper()):
	# 			temp=temp1[1]
	# 			temp=temp.strip()
	# 			#print(temp)
	# 			for i in range(2,len(temp1)):
	# 				next_sent=next_sent+temp1[i]
	# 				#print(next_sent)
	# 		temp1=[]

	# 	if temp in pattern_head4:
	# 		if key==-1:
	# 			key=temp
	# 		else:
	# 			dictionary[key]=clause
	# 			key=temp
	# 			clause=next_sent

	# 	else:
	# 		clause = re.sub(' +',' ',clause+sentence)


	# dictionary[key]= clause
	# return dictionary



def reader(file_url,getFullContract=False,extractionState=True):
	#Main function
	print (file_url)
	converted_pages = " "
	formatted_text = " "
	convert_contract = ContractStructure(file_url)
	# print("given path:",file_url)
	response_list = []
	current_pointer = os.getcwd()
	with open(file_url,'rb') as contract_reader:
		pdf = pdftotext.PDF(contract_reader)

		for pages in pdf:
			converted_pages = converted_pages + pages
	formatted_text = converted_pages
	contract_reader.close()
	# print (converted_pages)
	return formatted_text
