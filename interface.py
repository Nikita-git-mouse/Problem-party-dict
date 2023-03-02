import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QMenu, QAction
from pycparser import CParser
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

    def initUI(self):
        self.parserClass = CParser
        self.parse_button = QPushButton('Парсить')
        self.parse_file_button = QPushButton('Парсить файл')
        self.filter_button = QPushButton('Фильтровать')
        self.file_button = QPushButton('Выбрать файл')
        self.text_edit = QTextEdit()
        self.info_label = QLabel('Введите текст для парсинга')
        self.parts_of_speech_button = QPushButton('Части речи')
        self.parser = CParser
        self.help_button = QPushButton('Помощь')

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        left_layout.addWidget(self.parse_button)
        left_layout.addWidget(self.parse_file_button)
        left_layout.addWidget(self.filter_button)
        left_layout.addWidget(self.file_button)
        left_layout.addWidget(self.parts_of_speech_button)

        right_layout.addWidget(self.info_label)
        right_layout.addWidget(self.text_edit)
        left_layout.addWidget(self.help_button)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.result_text_edit = QTextEdit()
        self.result_text_edit.setReadOnly(True)
        self.help_button.clicked.connect(self.show_help)
        right_layout.addWidget(self.result_text_edit)
        self.parse_button.clicked.connect(self.parse_text)
        self.parse_file_button.clicked.connect(self.parse_file_text)
        self.filter_button.clicked.connect(self.filter_text)
        self.file_button.clicked.connect(self.open_file)
        self.parts_of_speech_button.clicked.connect(self.show_parts_of_speech_menu)
        self.setLayout(main_layout)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Приложение для парсинга текста')
        self.show()

    def parse_text(self):
        parsed_text = self.text_edit.toPlainText().split()
        if len(parsed_text) > 0:
            self.text = ' '.join(parsed_text)
            self.prepare_text()

            text = '\n'.join([f"{key}: {value}" for key, value in self.words_dict.items()][182:])
            self.result_text_edit.setText(text)
            self.text = ''
        else:
            pass

    def parse_file_text(self):
        text = '\n'.join([f"{key}: {value}" for key, value in self.words_dict.items()][1:182])
        self.result_text_edit.setText(text)

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
        """
        self.result_text_edit.setText(help_text)

    def prepare_text(self):
        """
        function to make all nessesary text's manipulations
        :return:
        """
        self.filter_text_pars()
        self.get_word_ending_list()
        self.get_word_info()

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
        pass
        # print('dict ',self.words_dict, len(self.words_dict))
        # print('normal form ', self.normal_form_dict)
        # print('info ', self.word_info_list)
        # print('base ', self.word_base_list)
        # print('endings', self.word_ending_dict)
        #  print('фильр', self.filtered_list)

    def get_lexeme_with_info(self):
        for word_index in range(len(self.words_dict)):
            print(self.word_list[word_index], self.word_base_list[word_index], self.word_info_list[word_index][0], self.word_ending_dict[self.word_base_list[word_index]])

    def everythingThatYouWant(self):
        MyWidget(self.open_file())
        self.prepare_text()
        self.show_info()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    with open('style.qss') as f:
        app.setStyleSheet(f.read())

    ex = MyWidget("Documents/example.pdf")
    ex.prepare_text()
    ex.show_info()
    sys.exit(app.exec_())
