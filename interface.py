import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QMenu, QAction
from pycparser import CParser

class MyWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.text_edit.setMouseTracking(True)

    def initUI(self):
       # создание виджетов
        self.parse_button = QPushButton('Парсить')
        self.filter_button = QPushButton('Фильтровать')
        self.file_button = QPushButton('Выбрать файл')
        self.text_edit = QTextEdit()
        self.info_label = QLabel('Введите текст для парсинга')
        self.parts_of_speech_button = QPushButton('Части речи')

        # создание лэйаутов
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # добавление виджетов в лэйауты
        left_layout.addWidget(self.parse_button)
        left_layout.addWidget(self.filter_button)
        left_layout.addWidget(self.file_button)
        left_layout.addWidget(self.parts_of_speech_button)

        right_layout.addWidget(self.info_label)
        right_layout.addWidget(self.text_edit)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # добавление нового виджета для вывода результата
        self.result_text_edit = QTextEdit()
        self.result_text_edit.setReadOnly(True)
        right_layout.addWidget(self.result_text_edit)

        # назначение обработчиков событий
        self.parse_button.clicked.connect(self.parse_text)
        self.filter_button.clicked.connect(self.filter_text)
        self.file_button.clicked.connect(self.open_file)
        self.parts_of_speech_button.clicked.connect(self.show_parts_of_speech_menu)

        # настройка главного окна
        self.setLayout(main_layout)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Приложение для парсинга текста')
        self.show()



    def parse_text(self):
        # обработка текста
        parsed_text = self.text_edit.toPlainText().split()
        parsed_text = '\n'.join(parsed_text)

        # вывод результата в новый виджет
        self.result_text_edit.setText(parsed_text)

    def filter_text(self):
        # обработка текста
        filtered_text = self.text_edit.toPlainText().replace(',', '').replace('.', '').replace('!', '').replace('?', '').replace('-', ' ')
        filtered_text = filtered_text.lower()

        # вывод результата в новый виджет
        self.result_text_edit.setText(filtered_text)

    def open_file(self):
        # открытие диалогового окна выбора файла
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "Text Files (*.txt)", options=options)

        # чтение текста из файла
        if file_name:
            with open(file_name, 'r') as file:
                file_text = file.read()

                # вывод текста в текстовое поле
                self.text_edit.setText(file_text)
                self.info_label.setText(f'Открыт файл: {file_name}')

    def show_parts_of_speech_menu(self):
        menu = QMenu(self)

        noun_action = QAction('Существительное', self)
        noun_action.triggered.connect(lambda: self.filter_by_part_of_speech('NOUN'))

        adj_action = QAction('Прилагательное', self)
        adj_action.triggered.connect(lambda: self.filter_by_part_of_speech('ADJ'))

        verb_action = QAction('Глагол', self)
        verb_action.triggered.connect(lambda: self.filter_by_part_of_speech('VERB'))

        menu.addAction(noun_action)
        menu.addAction(adj_action)
        menu.addAction(verb_action)

        menu.exec_(self.parts_of_speech_button.mapToGlobal(self.parts_of_speech_button.rect().bottomLeft()))

    def filter_by_part_of_speech(self, part_of_speech):
        # обработка текста
        filtered_text = self.text_edit.toPlainText().lower()
        filtered_text = ' '.join([word for word in filtered_text.split() if word.split('_')[-1] == part_of_speech])

        # вывод результата в новый виджет
        self.result_text_edit.setText(filtered_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')  # использовать стиль Fusion
    with open('style.qss') as f:
        app.setStyleSheet(f.read())  # применить стиль из файла style.qss

    ex = MyWidget()
    sys.exit(app.exec_())
