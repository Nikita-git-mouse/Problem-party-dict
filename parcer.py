from PyPDF2 import PdfReader
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.stem.snowball import RussianStemmer

import nltk
import spacy
import pymorphy2



from wiki_ru_wordnet import WikiWordnet
wikiwordnet = WikiWordnet()


from pymystem3 import Mystem

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


# nltk.download('universal_tagset')
# nltk.download('averaged_perceptron_tagger_ru')


class Parser:
    def __init__(self, filename):
        # init pdf file   "Documents/example.pdf"
        self.file = open(filename, 'rb')

        # read from file
        self.reader = PdfReader(self.file)
        # print(len(reader.pages))
        self.page = self.reader.pages[0]
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

        # -------- №2 ----------
        self.subordination_trees = []
        self.components_system = []



        # -------- #3 --------=
        self.normal_form_lists = []
        self.semantic_analysis_list_of_dicts = []



    def prepare_text(self):
        """
        function to make all nessesary text's manipulations
        :return:
        """
        # формируется список всех слов
        self.filter_text()
        # все списки и словари с инфой по словам заполняются
        self.get_word_info()
        # окончания слов?
        self.get_word_ending_list()

    def filter_text(self):
        """
        Формирует отсортированный по алфавиту список слов
        :return:
        """
        # get rid of necessary words
        self.stop_words = set(stopwords.words("russian"))
        for word in word_tokenize(self.text):
            if word.casefold() not in self.stop_words:
                self.filtered_list.append(word)

        # get rid of punctuation symbols
        filtered = list(filter(lambda x: x != ',' and x != '.' and x != ', ', self.filtered_list))
        self.filtered_list = list(filtered)

        # lowcase all the words and sort them
        self.filtered_list = sorted([x.lower() for x in self.filtered_list])

    # нужен ли этот метод вообще??
    def get_word_ending_list(self):
        print(self.word_list)
        for word in self.words_dict:
            # print('# ',self.stemmer.stem(word))
            buf_list = []
            # print(self.morph.parse(word)[0].inflect({'gent'}))
            for i in self.morph.parse(word)[0].lexeme:
                # print('= ', i.word)
                if self.stemmer.stem(word) in i.word:
                    # print('- ', i.word.replace(self.stemmer.stem(word),''))
                    buf_list.append(i.word.replace(self.stemmer.stem(word), ''))
            self.word_ending_dict[self.stemmer.stem(self.morph.parse(word)[0].word)] = buf_list

    def get_inflect_on_word_case(self, word, word_case, word_number):
        """
        Формирование словоформ по заданным числу и падежу
        :param word:
        :param word_case:
        :param word_number:
        :return:
        """
        try:
            if word_case == 'И.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'sing', 'nomn'}).word)
            elif word_case == 'И.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'plur', 'nomn'}).word)
            elif word_case == 'Р.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'gent'}).word)
            elif word_case == 'Р.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'plur', 'gent'}).word)
            elif word_case == 'Д.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'datv'}).word)
            elif word_case == 'Д.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'plur', 'datv'}).word)
            elif word_case == 'В.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'accs'}).word)
            elif word_case == 'В.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'plur', 'accs'}).word)
            elif word_case == 'Т.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'ablt'}).word)
            elif word_case == 'Т.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'plur', 'ablt'}).word)
            elif word_case == 'П.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'loct'}).word)
            elif word_case == 'П.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                print(self.morph.parse(word)[0].inflect({'plur', 'loct'}).word)
        except:
            pass

    def get_word_info(self):
        for token in self.filtered_list:
            if 'ЗПР' not in self.morph.parse(token)[0].tag.cyr_repr and 'НЕИЗВ' not in self.morph.parse(token)[0].tag.cyr_repr and 'ЧИСЛО' not in self.morph.parse(token)[0].tag.cyr_repr and 'Н' not in self.morph.parse(token)[0].tag.cyr_repr and 'ЧАСТ' not in self.morph.parse(token)[0].tag.cyr_repr and '-' not in self.morph.parse(token)[0].word:
                # теперь слова в list не повторяются! => 182 слова
                if self.morph.parse(token)[0].word not in self.words_dict.keys():
                    self.words_dict[self.morph.parse(token)[0].word] = self.morph.parse(token)[0].tag.cyr_repr.replace(',',' ').split()
                    self.word_list.append(self.morph.parse(token)[0].word)
                    # get word's NORMAL FORM
                    self.normal_form_dict[self.morph.parse(token)[0].word] = self.morph.parse(token)[0].normal_form
                    # add to the info list a list of each word info
                    self.word_info_list.append(self.morph.parse(token)[0].tag.cyr_repr.replace(',', ' ').split())
                    # get base of the word
                    self.word_base_list.append(self.stemmer.stem(self.morph.parse(token)[0].word))

    def show_info(self):
        print(len(self.words_dict), self.words_dict)
        print(len(self.normal_form_dict), self.normal_form_dict)
        print(len(self.word_info_list), self.word_info_list)
        print(len(self.word_base_list), self.word_base_list)
        print(len(self.word_ending_dict), self.word_ending_dict)

    def get_lexeme_with_info(self):
        for word_index in range(len(self.words_dict)):
            print(self.word_list[word_index], self.word_base_list[word_index], self.word_info_list[word_index][0],
                  self.word_ending_dict[self.word_base_list[word_index]])



    #------------------------------------------------№2----------------------------------------------
    import spacy
    from spacy import displacy

    def syntacic_analysis_subordination_trees(self):
        """
        Синтаксический разбор с помощью деревьев разбора
        :return:
        """
        nlp = spacy.load('ru_core_news_sm')
        # doc = nlp(self.text)
        doc = nlp('Это может оказаться единственным выходом.')

        # попробовала подобрать эти наборы букв под что-то более менее подходящее
        for token in doc:
            if token.dep_ == 'nsubj' or token.dep_ == 'nsubj:pass' or token.dep_ == 'csubj' or token.dep_ == 'xcomp':
                print(token.text, token.pos_,  'подлежащее')
                self.subordination_trees.append('подлежащее')
            elif token.dep_ == 'ROOT' or token.dep_ == 'conj' or token.dep_ == 'expl' or token.dep_ == 'parataxis' or token.dep_ == 'aux' or token.dep_ == 'ccomp':
                print(token.text, token.pos_, 'глагол')
                self.subordination_trees.append('глагол')
            elif token.dep_ == 'advmod' or token.dep_ == 'discourse' or token.dep_ == 'advcl':
                print(token.text, token.pos_, 'обстоятельство')
                self.subordination_trees.append('обстоятельство')
            elif token.dep_ == 'obj' or token.dep_ == 'nummod' or token.dep_ == 'obl' or token.dep_ == 'iobj' :
                print(token.text, token.pos_, 'дополнение')
                self.subordination_trees.append('дополнение')
            elif token.dep_ == 'nmod' or token.dep_ == 'amod'or token.dep_ == 'det' or token.dep_ == 'acl':
                print(token.text, token.pos_, 'определение')
                self.subordination_trees.append('определение')
            elif token.dep_ == 'cc' or token.dep_ == 'fixed' or token.dep_ == 'mark':
                print(token.text, token.pos_, 'союз')
                self.subordination_trees.append('союз')
            elif token.dep_ == 'case':
                print(token.text, token.pos_, 'предлог')
                self.subordination_trees.append('предлог')
            else:
                print(token.text, token.pos_, token.dep_)
                self.subordination_trees.append(token.dep_)



    def syntacic_analysis_component_systems(self):
        nlp = spacy.load('ru_core_news_sm')
        doc = nlp(self.text)
        # doc = nlp('В эти моменты отверженный превращается в беззащитного ребенка, он снова испытывает те же чувства, что в детстве, оказывается в том мире.')
        # take each sentence

        for sentence in doc.sents:
            # print(sentence)
            analysis_sentence = '('
            left_bracket, right_bracket = 1, 0
            for token in sentence:
                # if token.dep_ == 'cc' or token.dep_ == 'fixed' or token.dep_ == 'mark':
                #     pass
                    # if left_bracket:
                    #     left_bracket = False
                    #     l += f'{token.text})'
                    # elif not left_bracket:
                    #     left_bracket = True
                    #     l += f'({token.text}'

                if token.dep_ == 'punct':
                    if token.text != '.':
                        if left_bracket != right_bracket:
                            for i in range(left_bracket - right_bracket - 1):
                                analysis_sentence += ')'
                            right_bracket = left_bracket - 1
                            analysis_sentence += token.text  + ' ' + '('
                            right_bracket += 1
                            left_bracket += 1
                        elif left_bracket == right_bracket:
                            analysis_sentence += token.text + ' '  + '('
                            left_bracket += 1
                elif token.dep_ == 'nmod' or token.dep_ == 'amod'or token.dep_ == 'det' or token.dep_ == 'acl':
                    analysis_sentence += '(' + token.text + ' '
                    left_bracket += 1
                elif token.dep_ == 'case':
                    analysis_sentence += '(' + token.text + ' ' + '('
                    left_bracket += 2

                    # еще придумать проверку какую-нибудь

                else:
                    analysis_sentence += token.text + ' '
            if left_bracket != right_bracket:
                for i in range(left_bracket - right_bracket):
                    analysis_sentence += ')'
            analysis_sentence += '.'
            self.components_system.append(analysis_sentence)
            print(analysis_sentence)


    # ------------------------------------------ №3 --------------


    # w = gensim.models.Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
    def preprocess(self, text, stop_words, punctuation_marks, morph):
        print('---',text)
        tokens = word_tokenize(text)
        preprocessed_text = []
        for token in tokens:
            if token.casefold() not in self.stop_words:
                lemma = morph.parse(token)[0].normal_form
                preprocessed_text.append(lemma)
            # if token not in punctuation_marks:
            #     lemma = morph.parse(token)[0].normal_form
            #     if lemma not in self.stop_words:
            #         preprocessed_text.append(lemma)
        return preprocessed_text


    def semantic_analysis(self):
        for word in self.word_base_list:
            synsets = wikiwordnet.get_synsets(word)
            if len(synsets) != 0:
                dict = {}
                synonyms_list = []
                definition_dict = {}
                hypernyms_list = []
                hyponyms_list = []

                # синоним, определение
                synset = synsets[0]
                for syn in synset.get_words():
                    synonyms_list.append(syn.lemma())
                    definition_dict[syn.lemma()] = syn.definition()
                # гиперонимы
                for hypernym in wikiwordnet.get_hypernyms(synset):
                    for w in hypernym.get_words():
                        hypernyms_list.append(w.lemma())
                # гипонимы
                for hyponyms in wikiwordnet.get_hyponyms(synset):
                    for w in hyponyms.get_words():
                        hyponyms_list.append(w.lemma())
                print(dict)
                # fill the result list
                dict['word'] = word
                dict['synonyms'] = synonyms_list
                dict['definitions'] = definition_dict
                dict['hypernyms'] = hypernyms_list
                dict['hyponyms'] = hyponyms_list
                self.semantic_analysis_list_of_dicts.append(dict)
                print(dict)



if __name__ == '__main__':
    parser = Parser("Documents/example.pdf")
    # составляет все необходимые для дальнейшей работы словари и списки
    parser.prepare_text()

    # просто выводит все списки и словари в консоль
    # parser.show_info()

    # вот здесь вот меняются слова словечки по роду и числу->
    # parser.get_inflect_on_word_case('жаба', 'Р.п.', 'ед.ч.')
    # parser.get_inflect_on_word_case('человек', 'Р.п.', 'мн.ч.')


    # parser.syntacic_analysis_subordination_trees()
    # parser.syntacic_analysis_component_systems()



    # складывает все данные о синонимах и т.д. в список semantic_analysis_list_of_dicts
    parser.semantic_analysis()
