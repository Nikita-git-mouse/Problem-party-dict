from PyPDF2 import PdfReader
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')

file = open("D:\Kyrs3\EYZIS\Texts\Documents\example.pdf", 'rb')


reader = PdfReader(file)
print(len(reader.pages))
page = reader.pages[0]
text = page.extract_text()
# print(text)
# print(sent_tokenize(text))
# print(word_tokenize(text))



stop_words = set(stopwords.words("russian"))
filtered_list = []
for word in word_tokenize(text):
    if word.casefold() not in stop_words:
        filtered_list.append(word)
print(filtered_list)



class Parcer:
    def __init__(self, file):
        self.file = file
        self.reader = PdfReader(file)
        self.text = ''
        self.word_tokenize = []
        self.sent_tokenize = []

    def read_text_from_pdf(self):
        page = self.reader.pages[0]
        self.text = page.extract_text()
        self.sent_tokenize = sent_tokenize(self.text)
        self.word_tokenize = word_tokenize(self.text)

    def filter_text(self):
        stop_words = set(stopwords.words("russian"))
        filtered_list = []
        for word in self.word_tokenize:
            if word.casefold() not in stop_words:
                filtered_list.append(word)
        print(filtered_list)
