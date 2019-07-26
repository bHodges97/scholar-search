import scholarly
import csv

class Crawler():
    def __init__(self,query,limit = 50):
        search_query = scholarly.search_pubs_query(query)
        count = 0
        pubs = []
        fieldnames = ['abstract','author','eprint','title','url']
        for x in search_query:
            if 'eprint' in x.bib:
                with open("out.csv","a") as f:
                    csv.DictWriter(f, fieldnames=fieldnames).writerow(x.bib)
                count+=1
                if count == limit:
                    break

if __name__ == "__main__":
    c = Crawler("hpc")
