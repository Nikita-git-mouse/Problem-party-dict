from PyPDF2 import PdfReader
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.stem.snowball import RussianStemmer

import nltk
#import spacy
import pymorphy2


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
# nltk.download('universal_tagset')
# nltk.download('averaged_perceptron_tagger_ru')

# init pdf file
# file = open("Documents/example.pdf", 'rb')

# read from file
# reader = PdfReader(file)
# print(len(reader.pages))
# page = reader.pages[0]
# text = page.extract_text() # get text from file



# get rid of necessary words
# stop_words = set(stopwords.words("russian"))
# filtered_list = []
# for word in word_tokenize(text):
#     if word.casefold() not in stop_words:
#         filtered_list.append(word)
# print(filtered_list)

# steamer = PorterStemmer()


# get rid of punctuation symbols
# filtered = list(filter(lambda x: x != ',' and x != '.' and x != ', ', filtered_list))
# filtered = list(filtered)
# print(f)


# morph = pymorphy2.MorphAnalyzer()
# words_dict = {}
# normal_form_dict =[]
# word_info_list = []
#
# rs = RussianStemmer()
# word_base_list = []

# k = ['мама','Папа','арбуз','Яхта','олень']
# k = sorted([x.lower() for x in k])
# print(k)

# b = []
# for word in filtered:
#     b.append(word.lower())
#
# filtered = sorted(b)
# print(filtered)


#
# for token in filtered:
#     if 'ЗПР' not in morph.parse(token)[0].tag.cyr_repr and 'НЕИЗВ' not in morph.parse(token)[0].tag.cyr_repr and 'Н' not in morph.parse(token)[0].tag.cyr_repr and 'ЧАСТ' not in morph.parse(token)[0].tag.cyr_repr and '-' not in morph.parse(token)[0].word:
#         # print(morph.parse(token)[0].word ,morph.parse(token)[0].tag.cyr_repr) # get word and it's morph discription
#         # print(morph.parse(token))
#         words_dict[morph.parse(token)[0].word] = morph.parse(token)[0].tag.cyr_repr.replace(',',' ').split()
#         # nf_list.append(morph.parse(token)[0].inflect({'sing', 'nomn'}))
#         # print(morph.parse(token)[0].normal_form)
#         normal_form_dict.append(morph.parse(token)[0].normal_form)
#         # add to the info list a list of each word info
#         word_info_list.append(morph.parse(token)[0].tag.cyr_repr.replace(',',' ').split())
#         # get base of the word
#         word_base_list.append(rs.stem(morph.parse(token)[0].word))
#
#
#
# # отсортированный словарь слов с доп инфой
# print((words_dict.items()))
# # отсортированный список начальных форм слова
# print((normal_form_dict))
# print(word_info_list)
# print(word_base_list)


# for x in sorted(normal_form_dict):
#     try:
#         for i in morph.parse(x)[0].lexeme: # склонение слов по падежам
#             print('-', i.word, '-', i.tag.cyr_repr)
#     except:
#         print(morph.parse(x)[0].word)
    # print('3 - ', morph.parse(x)[0].make_agree_with_number(3).word)
    # print('4 - ', morph.parse(x)[0].make_agree_with_number(5).word)


class Parser:
    def __init__(self, filename):
        # init pdf file   "Documents/example.pdf"
        self.file = open(filename, 'rb')

        # read from file
        self.reader = PdfReader(self.file)
        # print(len(reader.pages))
        self.page = self.reader.pages[0]
        # self.text = 'текст'
        self.text = self.page.extract_text()  # get text from file

        self.morph = pymorphy2.MorphAnalyzer()
        self.stemmer = RussianStemmer()


        # all needed lists
        self.words_dict = {}
        self.word_list = []
        self.filtered_list = []
        self.normal_form_dict = {}
        self.word_info_list = []
        self.word_base_list = []
        self.word_ending_dict = {}


    def prepare_text(self):
        """
        function to make all nessesary text's manipulations
        :return:
        """
        self.filter_text()
        self.get_word_ending_list()
        self.get_word_info()


    def filter_text(self):
        # get rid of necessary words
        stop_words = set(stopwords.words("russian"))
        for word in word_tokenize(self.text):
            if word.casefold() not in stop_words:
                self.filtered_list.append(word)

        # get rid of punctuation symbols
        filtered = list(filter(lambda x: x != ',' and x != '.' and x != ', ', self.filtered_list))
        self.filtered_list = list(filtered)

        # lowcase all the words and sort them
        self.filtered_list = sorted([x.lower() for x in self.filtered_list])

    def get_word_ending_list(self):
        for word in self.words_dict:
            # print('# ',self.stemmer.stem(word))
            buf_list = []
            # print(self.morph.parse(word)[0].inflect({'gent'}))
            for i in self.morph.parse(word)[0].lexeme:
                # print('= ', i.word)
                if self.stemmer.stem(word) in i.word:
                    # print('- ', i.word.replace(self.stemmer.stem(word),''))
                    buf_list.append(i.word.replace(self.stemmer.stem(word),''))
            self.word_ending_dict[self.stemmer.stem(self.morph.parse(word)[0].word)] = buf_list

    def get_inflect_on_word_case(self, word, word_case, word_number):
        # print(self.morph.parse(token))
        try:
            if word_case == 'И.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'sing','nomn'}).word)
            elif word_case == 'И.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'plur','nomn'}).word)
            elif word_case == 'Р.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'gent'}).word)
            elif word_case == 'Р.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'plur','gent'}).word)
            elif word_case == 'Д.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'datv'}).word)
            elif word_case == 'Д.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'plur','datv'}).word)
            elif word_case == 'В.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'accs'}).word)
            elif word_case == 'В.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'plur','accs'}).word)
            elif word_case == 'Т.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'ablt'}).word)
            elif word_case == 'Т.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'plur','ablt'}).word)
            elif word_case == 'П.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'loct'}).word)
            elif word_case == 'П.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'plur','loct'}).word)
        except:
            pass


    def get_word_info(self):
        for token in self.filtered_list:
            if 'ЗПР' not in self.morph.parse(token)[0].tag.cyr_repr and 'НЕИЗВ' not in self.morph.parse(token)[0].tag.cyr_repr and 'ЧИСЛО' not in self.morph.parse(token)[0].tag.cyr_repr and 'Н' not in self.morph.parse(token)[0].tag.cyr_repr and 'ЧАСТ' not in self.morph.parse(token)[0].tag.cyr_repr and '-' not in self.morph.parse(token)[0].word:
                # print(morph.parse(token)[0].word ,morph.parse(token)[0].tag.cyr_repr) # get word and it's morph discription
                # print(self.morph.parse(token))
                self.words_dict[self.morph.parse(token)[0].word] = self.morph.parse(token)[0].tag.cyr_repr.replace(',',' ').split()
                self.word_list.append(self.morph.parse(token)[0].word)
                # get word's NORMAL FORM
                self.normal_form_dict[self.morph.parse(token)[0].word] = self.morph.parse(token)[0].normal_form
                # add to the info list a list of each word info
                self.word_info_list.append(self.morph.parse(token)[0].tag.cyr_repr.replace(',',' ').split())
                # get base of the word
                self.word_base_list.append(self.stemmer.stem(self.morph.parse(token)[0].word))


    def show_info(self):
        print('dict ', self.words_dict, len(self.words_dict))
        # print('normal form ', self.normal_form_dict)
        # print('info ', self.word_info_list)
        # print('base ', self.word_base_list)
        # print('endings', self.word_ending_dict)
       #  print('фильр', self.filtered_list)


    def get_lexeme_with_info(self):
        for word_index in range(len(self.words_dict)):
            print(self.word_list[word_index], self.word_base_list[word_index], self.word_info_list[word_index][0], self.word_ending_dict[self.word_base_list[word_index]])


if __name__ == '__main__':
    parser = Parser("Documents/example.pdf")
    parser.prepare_text()
    parser.show_info()
    # parser.show_info()
    # parser.get_lexeme_with_info()



