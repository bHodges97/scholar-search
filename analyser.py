from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, strip_accents_unicode

from os import walk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords as nltk_stopwords
import subprocess

class Analyser():
    def analyse(self):
        stopwords = frozenset(nltk_stopwords.words('english'))#very slow if not set
        files = [f'downloads/{x}' for x in list(walk('downloads'))[0][2]]
        vectorizer = CountVectorizer(preprocessor=Analyser.preprocess,
                analyzer="word",
                tokenizer=Analyser.tokenizer,
                stop_words=[])
        x = vectorizer.fit_transform(files)
        print(vectorizer.get_feature_names())

    def preprocess(path):
        text = Analyser.file_to_text(path)
        text = text.lower()
        text = strip_accents_unicode(text)
        return text

    def tokenizer(text):
        tokens = word_tokenize(text)
        tokens = filter(lambda x:x.isalpha(),tokens)
        return tokens

    def file_to_text(path):
        filetype = subprocess.run(["file","-b",path], stdout=subprocess.PIPE).stdout.decode('utf-8')
        if filetype.startswith("PDF"):
            cmd = ["pdftotext",path,"-"]
        elif filetype.startswith("HTML"):
            cmd = ["html2text",path]
        else:
            cmd = ['cat']
        result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout
        return result.decode('utf-8')



if __name__ == "__main__":
    a = Analyser()
    a.analyse()




