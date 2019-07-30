crawler.py
  - searches google scholar, saves bib entries to out.csv
  - download() loads out.csv and tries to download pdfs

analyser.py
  - list files in download folder
  - files -> lowercase -> ascii -> tokenize -> remove stop words -> count vectorise| 4.5 sec
  - count vector -> tfidf transform -> svd| 0.02 sec
  - svd -> minibatch kmeans | 0.03 sec
