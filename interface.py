import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QMenu, QAction
from pycparser import CParser
from PyPDF2 import PdfReader
from anytree import Node, RenderTree

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.stem.snowball import RussianStemmer

from nltk.stem.snowball import RussianStemmer
from nltk.corpus import stopwords

import nltk
import spacy
import pymorphy2


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


class MyWidget(QWidget):

    def __init__(self, filename):
        super().__init__()
        self.initUI()
        self.text_edit.setMouseTracking(True)
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

    def initUI(self):
        self.parserClass = CParser
        self.parse_button = QPushButton('Парсить')
        self.parse_file_button = QPushButton('Парсить файл')
        self.filter_button = QPushButton('Фильтровать')
        self.file_button = QPushButton('Выбрать файл')

        self.text_edit = QTextEdit()
        self.info_label = QLabel('Введите текст для парсинга')
        self.parts_of_speech_button = QPushButton('Части речи')

        self.changeParams = QPushButton('Преобразование')
        self.parser = CParser
        self.help_button = QPushButton('Помощь')

        self.filter_button = QPushButton('Фильтровать')
        self.file_button = QPushButton('Выбрать файл')
        # ----------------------Treeeeeeee---------------

        self.Tree_button = QPushButton('Дерево Форм')
        self.Analysis_button = QPushButton('Синнтаксический разбор')


        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        left_layout.addWidget(self.parse_button)
        left_layout.addWidget(self.parse_file_button)
        left_layout.addWidget(self.filter_button)
        left_layout.addWidget(self.changeParams)
        left_layout.addWidget(self.file_button)
        left_layout.addWidget(self.parts_of_speech_button)
        #  ---- 2 ----
        left_layout.addWidget(self.Tree_button)
        left_layout.addWidget(self.Analysis_button)

        right_layout.addWidget(self.info_label)
        #right_layout.addWidget(self.text_edit)
        left_layout.addWidget(self.help_button)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.result_text_edit = QTextEdit()
        self.result_text_edit.setReadOnly(True)
        self.help_button.clicked.connect(self.show_help)
        right_layout.addWidget(self.result_text_edit)
        self.parse_button.clicked.connect(self.parse_text)
        self.changeParams.clicked.connect(self.changeForm)
        self.parse_file_button.clicked.connect(self.parse_file_text)
        self.filter_button.clicked.connect(self.filter_text)
        self.file_button.clicked.connect(self.open_file)
        self.parts_of_speech_button.clicked.connect(self.show_parts_of_speech_menu)
        self.setLayout(main_layout)

        # ----- 2 ----
        self.Tree_button.clicked.connect(self.syntacic_analysis_component_systems)
        self.Analysis_button.clicked.connect(self.syntacic_analysis_subordination_trees)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Приложение для парсинга текста')
        self.show()



    def show_info(self):
            print('dict ', self.words_dict)
            print('normal form ', self.normal_form_dict)
            print('info ', self.word_info_list)
            print('base ', self.word_base_list)
            print('endings', self.word_ending_dict)

    def parse_text(self):
        parsed_text = self.text_edit.toPlainText().split()
        if len(parsed_text) > 0:
            self.text = ' '.join(parsed_text)
            self.prepare_text()
            info = '\n'.join([f"{key}: {value}" for key, value in self.words_dict.items()][182:])
            self.result_text_edit.setText(info)
            self.text = ''
        else:
            pass


    def get_one_word_ending_list(self, word):
        # print('# ',self.stemmer.stem(word))
        buf_list = []
        # print(self.morph.parse(word)[0].inflect({'gent'}))
        for i in self.morph.parse(word)[0].lexeme:
            # print('= ', i.word)
            if self.stemmer.stem(word) in i.word:
                # print('- ', i.word.replace(self.stemmer.stem(word),''))
                buf_list.append(i.word.replace(self.stemmer.stem(word),''))
        self.word_ending_dict[self.stemmer.stem(self.morph.parse(word)[0].word)] = buf_list

    def parse_file_text(self):
        dict = list(self.words_dict.items())
        normal_form = list(self.normal_form_dict.items())
        base = self.word_base_list
        array = []
        print(self.words_dict.keys())
        # if 'ачинают' in self.words_dict:
        #     del self.words_dict['ачинают']
        a = set(list((self.word_base_list)))
        print(len(self.word_base_list))
        print(len(a))
        endings = iter(self.words_dict.keys())
        for i in range(1, 181):
            ending = next(endings)
            ending_len = len(self.word_ending_dict)
            self.get_one_word_ending_list(ending)
            new_param = self.word_list
            new_info = self.word_info_list
            new_ending_len = len(self.word_ending_dict)
            last_key, last_value = list(self.word_ending_dict.items())[-1]

            if new_ending_len > ending_len:
                array.append([f'{new_param[i]}\nСвойства {new_info[i]}\nНормальная форма {normal_form[i]}\nОснова слова "{base[i]}"\nОкончания {last_key, last_value}\n'])
            else:
                print(len(self.word_ending_dict))
                array.append([f'Свойства {new_info[i]}\nНормальная форма {normal_form[i]}\nОснова слова "{base[i]}"\n'])

        print()
        # print(len(dict), len(normal_form), len(base), len(endings))
        string_result = '\n'.join(', '.join(str(x) for x in row) for row in array)
        lexemes_with_info = self.get_lexeme_with_info()

        # Create a string with each element of the array on a new line
        output_string = ''
        for lexeme in lexemes_with_info:
            output_string += str(lexeme) + '\n' + '\n'

        # Set the text of the result text edit widget to the output string
        self.result_text_edit.setText(output_string)
       # self.result_text_edit.setText(str(self.get_lexeme_with_info()))
        if os.path.isfile('НеБезПрикола.txt'):
            pass
        else:
            with open('НеБезПрикола.txt', 'w') as f:
                f.write(output_string)

        self.word_ending_dict = {}

    def showInputImportantInformation(self):
        pass

    def changeForm(self):
        parsed_text = self.text_edit.toPlainText().split()
        print(parsed_text)
        print(len(parsed_text))
        if len(parsed_text) == 3:
            result = self.get_inflect_on_word_case(parsed_text[0], parsed_text[1], parsed_text[2])
            self.words_dict = {result}
            self.result_text_edit.setText(result)
        else:
            pass

    def filter_text(self):
        newdict = {}
        smthParams = self.text_edit.toPlainText().split()
        if len(smthParams) > 0:
            for key, value in self.words_dict.items():
                if smthParams[0] in value:
                    newdict[key] = value
            text = '\n'.join([f"{key}: {value}" for key, value in newdict.items()])
            self.result_text_edit.setText(text)
        pass

    def open_file(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "Text Files (*.pdf)", options=options)



    def show_parts_of_speech_menu(self):
        menu = QMenu(self)

        noun_action = QAction('Существительное', self)
        noun_action.triggered.connect(lambda: self.filter_by_part_of_speech('СУЩ'))

        adj_action = QAction('Прилагательное', self)
        adj_action.triggered.connect(lambda: self.filter_by_part_of_speech('ПРИЛ'))

        verb_action = QAction('Глагол', self)
        verb_action.triggered.connect(lambda: self.filter_by_part_of_speech('ГЛ'))

        menu.addAction(noun_action)
        menu.addAction(adj_action)
        menu.addAction(verb_action)

        menu.exec_(self.parts_of_speech_button.mapToGlobal(self.parts_of_speech_button.rect().bottomLeft()))

    def filter_by_part_of_speech(self, part_of_speech):
        newdict = {}
        for key, value in self.words_dict.items():
            if part_of_speech in value:
                newdict[key] = value
        text = '\n'.join([f"{key}: {value}" for key, value in newdict.items()])
        self.result_text_edit.setText(text)

    def show_help(self):
        help_text = """
        Использование приложения:
        1. Нажмите на кнопку "Выбрать файл" для открытия текстового файла или введите текст в поле "Введите текст для парсинга".
        2. Нажмите на кнопку "Парсить" для обработки текста с помощью парсера.
        3. Нажмите на кнопку "Части речи" для фильтрации текста по частям речи.
        4. Введите слова для фильтрации в поле "Фильтровать" и нажмите на кнопку "Фильтровать" для фильтрации текста.
        5. Введите в поле слово для преобразования, падеж (Р.п.), число (ед.ч.) через пробел
        """
        self.result_text_edit.setText(help_text)

    def prepare_text(self):
        """
        function to make all nessesary text's manipulations
        :return:
        """
        self.filter_text_pars()
        self.get_word_info()
        #self.get_word_ending_list()

    def filter_text_pars(self):
        # get rid of necessary words
        stop_words = set(stopwords.words("russian"))
        for word in word_tokenize(self.text):
            if word.casefold() not in stop_words:
                self.filtered_list.append(word)
        filtered = list(filter(lambda x: x != ',' and x != '.' and x != ', ', self.filtered_list))
        self.filtered_list = list(filtered)
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
                return self.morph.parse(word)[0].inflect({'sing','nomn'}).word
            elif word_case == 'И.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                return self.morph.parse(word)[0].inflect({'plur','nomn'}).word
            elif word_case == 'Р.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                return self.morph.parse(word)[0].inflect({'gent'}).word
            elif word_case == 'Р.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                return self.morph.parse(word)[0].inflect({'plur','gent'}).word
            elif word_case == 'Д.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                return self.morph.parse(word)[0].inflect({'datv'}).word
            elif word_case == 'Д.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                return self.morph.parse(word)[0].inflect({'plur','datv'}).word
            elif word_case == 'В.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                return self.morph.parse(word)[0].inflect({'accs'}).word
            elif word_case == 'В.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                return self.morph.parse(word)[0].inflect({'plur','accs'}).word
            elif word_case == 'Т.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                return self.morph.parse(word)[0].inflect({'ablt'}).word
            elif word_case == 'Т.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                return self.morph.parse(word)[0].inflect({'plur','ablt'}).word
            elif word_case == 'П.п.' and word_number == 'ед.ч.':
                # for token in self.word_list:
                return self.morph.parse(word)[0].inflect({'loct'}).word
            elif word_case == 'П.п.' and word_number == 'мн.ч.':
                # for token in self.word_list:
                return self.morph.parse(word)[0].inflect({'plur','loct'}).word
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

    def get_lexeme_with_info(self):
        array = []
        for word_index in range(1, len(self.words_dict)):
            array.append(f'Слово:{self.word_list[word_index]}, \nОснова:{self.word_base_list[word_index]}, \nСвойства:{self.word_info_list[word_index]},\nОкончания:{self.word_ending_dict[self.word_base_list[word_index]]}')
        return array

    def everythingThatYouWant(self):
        MyWidget(self.open_file())
        self.prepare_text()
        self.show_info()


#------------------------------------------------№2----------------------------------------------
    import spacy
    from spacy import displacy

    def syntacic_analysis_subordination_trees(self):
        """
        Синтаксический разбор с помощью деревьев разбора
        :return:
        """
        analResult = []
        nlp = spacy.load('ru_core_news_sm')
        doc = nlp(self.text)
        #doc = nlp('Это может оказаться единственным выходом.')
        # попробовала подобрать эти наборы букв под что-то более менее подходящее
        for token in doc:
            if token.dep_ == 'nsubj' or token.dep_ == 'nsubj:pass' or token.dep_ == 'csubj' or token.dep_ == 'xcomp':
                analResult.append([token.text, token.pos_,  'подлежащее'])
                self.subordination_trees.append('подлежащее')
            elif token.dep_ == 'ROOT' or token.dep_ == 'conj' or token.dep_ == 'expl' or token.dep_ == 'parataxis' or token.dep_ == 'aux' or token.dep_ == 'ccomp':
                analResult.append([token.text, token.pos_, 'глагол'])
                self.subordination_trees.append('глагол')
            elif token.dep_ == 'advmod' or token.dep_ == 'discourse' or token.dep_ == 'advcl':
                analResult.append([token.text, token.pos_, 'обстоятельство'])
                self.subordination_trees.append('обстоятельство')
            elif token.dep_ == 'obj' or token.dep_ == 'nummod' or token.dep_ == 'obl' or token.dep_ == 'iobj' :
                analResult.append([token.text, token.pos_, 'дополнение'])
                self.subordination_trees.append('дополнение')
            elif token.dep_ == 'nmod' or token.dep_ == 'amod'or token.dep_ == 'det' or token.dep_ == 'acl':
                analResult.append([token.text, token.pos_, 'определение'])
                self.subordination_trees.append('определение')
            elif token.dep_ == 'cc' or token.dep_ == 'fixed' or token.dep_ == 'mark':
                analResult.append([token.text, token.pos_, 'союз'])
                self.subordination_trees.append('союз')
            elif token.dep_ == 'case':
                analResult.append([token.text, token.pos_, 'предлог'])
                self.subordination_trees.append('предлог')
            else:
                analResult.append([token.text, token.pos_, token.dep_])
                self.subordination_trees.append(token.dep_)
        output_text = ""
        for i in range(len(analResult)):
            word = f"{analResult[i][0]} - {analResult[i][2]}"
            output_text += word + "\n"
            if analResult[i][2] == "punct" and analResult[i][0] != ",":
                output_text += "\n"

        self.result_text_edit.setText(output_text)


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

        result = self.components_system
        output = '\n'.join(result).replace('.', '.\n')
        self.result_text_edit.setText(output)

    def build_tree(self, data, parent=None):
        for item in data:
            if isinstance(item, tuple):
                node = Node(item[0], parent=parent)
                self.build_tree(item[1], parent=node)
            else:
                Node(item, parent=parent)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    with open('style.qss') as f:
        app.setStyleSheet(f.read())

    ex = MyWidget("Documents/example.pdf")
    ex.prepare_text()
    #ex.show_info()
    sys.exit(app.exec_())
