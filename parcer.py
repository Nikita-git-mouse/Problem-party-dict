from PyPDF2 import PdfReader
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.stem.snowball import RussianStemmer

import nltk
import spacy


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
# nltk.download('universal_tagset')
# nltk.download('averaged_perceptron_tagger_ru')

# init pdf file
file = open("Documents/example.pdf", 'rb')

# read from file
reader = PdfReader(file)
print(len(reader.pages))
page = reader.pages[0]
text = page.extract_text() # get text from file
# print(text)
# print(sent_tokenize(text))
# print(word_tokenize(text))


# get rid of necessary words
stop_words = set(stopwords.words("russian"))
filtered_list = []
for word in word_tokenize(text):
    if word.casefold() not in stop_words:
        filtered_list.append(word)
# print(filtered_list)

# steamer = PorterStemmer()


# get rid of punctuation symbols
filtered = list(filter(lambda x: x != ',' and x != '.' and x != ', ', filtered_list))
filtered = list(filtered)
# print(f)

import pymorphy2
morph = pymorphy2.MorphAnalyzer()
words_dict = {}
normal_form_list =[]

for token in filtered:
    if 'ЗПР' not in morph.parse(token)[0].tag.cyr_repr and 'НЕИЗВ' not in morph.parse(token)[0].tag.cyr_repr and 'Н' not in morph.parse(token)[0].tag.cyr_repr and 'ЧАСТ' not in morph.parse(token)[0].tag.cyr_repr and '-' not in morph.parse(token)[0].word:
        # print(morph.parse(token)[0].word ,morph.parse(token)[0].tag.cyr_repr) # get word and it's morph discription
        words_dict[morph.parse(token)[0].word] = morph.parse(token)[0].tag.cyr_repr
        # nf_list.append(morph.parse(token)[0].inflect({'sing', 'nomn'}))
        # print(morph.parse(token)[0].normal_form)
        normal_form_list.append(morph.parse(token)[0].normal_form)
        # print('- ',morph.parse(token)[0].make_agree_with_number(1).word)


# sorted(words_dict.keys())
# sorted_words_dict = sorted(words_dict)
print(sorted(words_dict.items()))
print(sorted(normal_form_list))
for x in sorted(normal_form_list):
    try:
        for i in morph.parse(x)[0].lexeme:
            print('-', i.word, '-', i.tag.cyr_repr)
    except:
        print(morph.parse(x)[0].word)
    # print('3 - ', morph.parse(x)[0].make_agree_with_number(3).word)
    # print('4 - ', morph.parse(x)[0].make_agree_with_number(5).word)




# rs = RussianStemmer()
# print(rs.stem('полиграфы'))
# s = [rs.stem(word) for word in f]
# print(list(s))
#
#
#
#
#
#
# voc = nltk.tag.pos_tag(f,lang='rus')
# print(voc)
#
# lemmatizer = WordNetLemmatizer()
# print(lemmatizer.lemmatize('яблоки'))
#
#
# from spacy.lang.ru.examples import sentences
#
# nlp_ru = spacy.load("ru_core_news_sm")
# doc = nlp_ru(text)
# print(type(text))
# print(type(f[0]))
# for t in doc:
#     print(t.text, t.pos_)


# узнать часть речи
# for pare in voc:
#
#     if pare[1] == 'S':
#         print(pare, 'существительное')
#     elif pare[1] == 'V':
#         print(pare, 'глагол')
#     elif pare[1] == 'ADV':
#         print(pare, 'прилагательное')
#     elif pare[1] == 'A=m':
#         print(pare, 'краткое причастие')
#     elif pare[1] == 'A-PRO=pl':
#         print(pare, 'причастие')
#     s = pare[0]
#
#     if pare[0][len(pare[0])-1] == 'о':
#
#         print(pare, 'наречие')







class Parcer:
    def __init__(self, file):
        self.file = ''
        self.reader = PdfReader(file)
        self.text = ''
        self.word_tokenize = []
        self.sent_tokenize = []

    # get text from the pdf file
    def read_text_from_pdf(self, file):
        self.file = file
        page = self.reader.pages[0]
        self.text = page.extract_text()
        self.sent_tokenize = sent_tokenize(self.text)
        self.word_tokenize = word_tokenize(self.text)

    # filter stopwords out of the text
    def filter_text(self):
        stop_words = set(stopwords.words("russian"))
        filtered_list = []
        for word in self.word_tokenize:
            if word.casefold() not in stop_words:
                filtered_list.append(word)
        print(filtered_list)
        return filtered_list

    def stemm_text(self):
        pass

