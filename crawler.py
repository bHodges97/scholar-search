import scholarly
import csv
import http.cookiejar
from urllib.request import urlopen, Request, build_opener, HTTPCookieProcessor
from urllib.error import HTTPError
from os import walk
from pdffinder import PDFFinder
from urllib.parse import urlparse


from sklearn.feature_extraction.text import TfidfVectorizer

class Crawler():
    def __init__(self):
        #pretend to be browser to avoid 403 error
        self.header = ('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0')
        self.headers = {self.header[0]:self.header[1]}
        self.outfile = "out.csv"

    def url_name(self,url):
        if url[-1] == '/':
            url = url[:-1]
        return url.split('/')[-1]

    def fix_url(self,url):
        if url[0] == '/':
            url = "https://scholar.google.co.uk" + url
        return url

    def query(self,query,limit = 50):
        search_query = scholarly.search_pubs_query(query)
        count = 0
        pubs = []
        self.files = []
        fieldnames = ['abstract','author','eprint','title','url']
        with open(self.outfile,"w") as f:
            f.write(",".join(fieldnames) + "\n")
        for x in search_query:
            if 'eprint' in x.bib:
                with open(self.outfile,"a") as f:
                    csv.DictWriter(f, fieldnames=fieldnames).writerow(x.bib)
                count+=1
                if count == limit:
                    break

    def download(self):
        cj = http.cookiejar.CookieJar()
        opener = build_opener(HTTPCookieProcessor(cj))
        opener.addheaders = [self.header]
        print(opener.addheaders)
        with open(self.outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = self.fix_url(row['eprint'])
                parsed_uri = urlparse(url)
                root = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
                file_path = "downloads/"+self.url_name(url)
                try:
                    print(row['title'])
                    with opener.open(url) as res:
                        content_type = res.info().get_content_subtype()
                        page = res.read()
                        if content_type == "html" and row['eprint'][0] != '/':
                            page = self.html_to_pdf(page,opener,root)
                        else:
                            print("Download:",url)
                    if page == None:
                        continue
                    with open(file_path, "wb") as fp:
                        fp.write(page)
                        print("Success")
                except HTTPError as err:
                    print("Error", err.code)
                except ConnectionError as err:
                    print(err)

    def html_to_pdf(self,page,opener,root):
        html = ascii(page) #.decode("utf-8") not all pages are unicode
        finder = PDFFinder()
        finder.feed(html)
        url = finder.pdflink()
        if url == "":
            print("Download: Not found")
            return None
        elif url[0] == "/":
            url = root+url
        print("Download:",url)
        with opener.open(url) as res:
            content_type = res.info().get_content_subtype()
            page = res.read()
            if content_type != "pdf":
                print("Not pdf",content_type)
                return None
        return page




    def analyse(self):
        for root, dirs, files in walk('downloads'):
            print(root,len(files))


if __name__ == "__main__":
    c = Crawler()
    #c.query("hpc")
    c.download()
    c.analyse()
