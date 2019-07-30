from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, strip_accents_unicode
from sklearn.cluster import KMeans,MiniBatchKMeans
from sklearn.decomposition import TruncatedSVD
from sklearn import metrics
from os import walk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords as nltk_stopwords
from time import time
import subprocess

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Analyser():
    def analyse(self,clusters=5,verbose=False):
        t0 = time()
        stopwords = frozenset(nltk_stopwords.words('english'))#very slow if not set
        filenames = [x for x in list(walk('downloads'))[0][2]]
        files = [f'downloads/{x}' for x in filenames]
        vectorizer = CountVectorizer(preprocessor=Analyser.preprocess,
                analyzer="word",
                tokenizer=Analyser.tokenizer,
                stop_words=[],
#               max_df=0.5,#ignore top 50%
                min_df=2,
                max_features=10000)
        tf = vectorizer.fit_transform(files)
        t1 = time()
        tfidfTransformer = TfidfTransformer()
        tfidf = tfidfTransformer.fit_transform(tf)
        svd = TruncatedSVD(n_components=2)
        reduced = svd.fit_transform(tfidf)
        t2 = time()
        km = MiniBatchKMeans(n_clusters=clusters, init='k-means++', n_init=1, init_size=1000, batch_size=1000, verbose=verbose)
        #km = KMeans(n_clusters=clusters, init='k-means++', max_iter=100, n_init=1, verbose=verbose)
        km.fit(reduced)
        centers = km.cluster_centers_
        y_kmeans = km.predict(reduced)
        t3 = time()
        print(t3-t0,t1-t0,t2-t1,t3-t2)
        ax = plt.figure().add_subplot(111)#, projection='3d')
        ax.scatter(reduced[:, 0], reduced[:, 1], c=y_kmeans,  cmap='viridis')
        ax.scatter(centers[:, 0], centers[:, 1], c='red', marker='x', alpha=0.5);
        for i in range(40):
            ax.annotate(filenames[i][3:],reduced[i])
        plt.show()



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




