crawler.py
  - searches google scholar, saves bib entries to out.csv
  - download() loads out.csv and tries to download pdfs

analyser.py
  - list files in download
  - files -> lowercase -> ascii -> tokenize -> remove stop words | 4.16 sec
  - tokens -> count vectorise -> tfidf transform | 0.003 sec
  - tfidf -> svd -> minibatch kmeans | 0.07 sec
