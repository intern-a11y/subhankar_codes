
import os
import re
import pandas as pd
# from main import extract
import pickle
from sentence_transformers import SentenceTransformer
import scipy.spatial

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
# embedder = SentenceTransformer('bert-base-nli-mean-tokens')
embedder = SentenceTransformer('bert-large-nli-stsb-mean-tokens')




REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]"')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_*]')
# Corpus with example sentences
# corpus = ['LEASE AGREEMENT This LEASE AGREEMENT this Lease  dated as of October 1 2017 is made by and between i THE OLGA BAKER TRUST DATED DECEMBER 26, 2012 AND AMENDED ON MARCH 5, 2014, TRUST B UNDER ARTICLE 8 OF THE LAST WILL AND TESTAMENT OF PAUL N. BAKER and LAWRENCE J. BAKER (collectively, “Landlord”), on the one hand, and HUB INTERNATIONAL NORTHWEST LLC, a Washington limited liability company (“Tenant”), on the other hand.',
#           'THIS CONSULTING AGREEMENT (this "Agreement") is made and entered into effective as of the first day of January 2013, between Inter Parfums, Inc., a Delaware corporation (“Company”), with offices at 551 Fifth Avenue, New York, NY 10176, and Jean Madar Holding SAS, a French corporation (“Consultant”) with its offices at c/o Fonciere du rond point 67, rue de la Boétie 75008 Paris, France.',
#           'FOR VALUE RECEIVED, G OPHER P ROTOCOL I NC ., a Nevada corporation (“Borrower”), promises to pay in lawful money of the United States of America to the order of I LIAD R ESEARCH AND T RADING , L.P., a Utah limited partnership, or its successors or assigns (“Lender”), the principal sum of $2,325,000.00, together with all other amounts due under this Promissory Note (this “Note”). This Note is issued pursuant to that certain Note Purchase Agreement of even date herewith between Borrower and Lender (the “Purchase Agreement”).',
#           'THIS EMPLOYMENT AGREEMENT (“Agreement”) is entered into by and between William B. Ridenour (“Executive”) and ANGI Homeservices, Inc., a Delaware corporation (the “Company”), and is effective as of November 8, 2018 (the “Effective Date”).',
#           'This Equipment Lease Agreement (“Agreement”) is made and entered into effective as of October 21, 2014 (the “Effective Date”) by and between: PERKIN INDUSTRIES, LLC, a Louisiana limited liability company having its principal place of business at 342 Walnut Street, New Orleans, Louisiana, 70118 (“Lessor”); and U-VEND, INC. (OTC: UVND), a Delaware corporation, with its principal place of business located at: 1507 7 th Street, Unit 425, Santa Monica, CA 90401 (“Lessee”).',
#           'This LICENSE AGREEMENT (the “AGREEMENT”) is made and executed as of May 15, 2003, by and between HARD ROCK HOTEL LICENSING, INC., a Florida corporation (“LICENSOR”), and PREMIER ENTERTAINMENT, LLC, a Mississippi limited liability company (“LICENSEE”).',
#           'THIS LOAN AGREEMENT (as amended, modified or supplemented from time to time, together with all exhibits, schedules, annexes and other attachments hereto, this “Agreement”) is entered into as of November 28, 2018, between SunStrong 2018-1 Mezzanine, LLC, a Delaware limited liability company (the “Borrower”), and SunStrong Capital Lender LLC, a Maryland limited liability company (together with its successors and assigns, the “Lender”). Capitalized terms have the meanings set forth in Article 1 of this Agreement.',
#           ]
def clean_text(text):
    """
        text: a string

        return: modified initial string
    """
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text. substitute the matched string in REPLACE_BY_SPACE_RE with space.
    text = BAD_SYMBOLS_RE.sub('', text) # remove symbols which are in BAD_SYMBOLS_RE from text. substitute the matched string in BAD_SYMBOLS_RE with nothing.
    return text


# data = []
df = pd.read_csv("audit_clause_bert_corpus.csv")

# instruction = df.instruction.values

# print(instruction)

corpus = df["instruction"][0:len(df["instruction"]) - 172]


#
#
# for d in data:
#     text_str = clean_text(d.lower())
#     text_str = text_str.replace('\n', ' ')
#     text_str = re.sub("\\.+",' ',text_str)
#     text_str = re.sub('_+', ' ', text_str)
#     # sent_2 = re.sub('-+', ' ', sent_1)
#     text_str = re.sub(' +', ' ', text_str)
#     corpus.append(text_str)



# [corpus.append(clean_text(d.lower())) for d in data]


# print(corpus)

corpus_embeddings = embedder.encode(corpus)


def bert_similarity_score(query_sentence):


    query_sentence = re.sub('\d',' ', query_sentence)
    query_sentence = re.sub(' +', ' ', query_sentence)
    query_sentence = clean_text(query_sentence)

    queries = []
    queries.append(query_sentence)

    #
    query_embeddings = embedder.encode(queries)
    scores = []

    # closest_n = 5
    for query, query_embedding in zip(queries, query_embeddings):
        distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]

        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])

        # for idx, distance in results[0:closest_n]:
        for idx, distance in results:
            # print(corpus[idx].strip(), "(Score: %.4f)" % (1-distance))
            scores.append(1-distance)

        return sum(scores)
