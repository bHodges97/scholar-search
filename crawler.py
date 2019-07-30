import scholarly
import csv
import http.cookiejar
from urllib.error import HTTPError
from pdffinder import *
from urllib.parse import urlparse
from requests.exceptions import TooManyRedirects
import requests




class Crawler():
    def __init__(self):
        #pretend to be browser to avoid 403 error
        self.headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'}
        self.outfile = "out.csv"

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
        self.jar = requests.cookies.RequestsCookieJar()
        with open(self.outfile) as csvfile:
            reader = csv.DictReader(csvfile)
            for idx,row in enumerate(reader):
                if row['eprint'][0] == '/':
                    res = requests.get("https://scholar.google.co.uk"+url,headers=self.headers,cookies=self.jar)
                    rg = LibraryLink()
                    rg.feed(ascii(res.content))
                    url = "http://zp2yn2et6f.scholar.serialssolutions.com/" + rg.link[1:]
                    print("Library link")
                    continue
                parsed_uri = urlparse(url)
                root = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
                file_path = "downloads/{:05d}.pdf".format(idx)
                try:
                    print(row['title'])
                    res = requests.get(url,headers=self.headers,cookies=self.jar) # set stream=True for chunk by chunk
                    content_type = res.headers['content-Type']
                    page = res.content
                    if "html" in content_type:
                        page = self.html_to_pdf(page, root)
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
                except TooManyRedirects as err:
                    print(err)

    def html_to_pdf(self,page,root,depth=0):
        html = ascii(page) #.decode("utf-8") not all pages are unicode
        finder = PDFFinder()
        finder.feed(html)
        url = finder.pdflink()
        if url == "":
            print("Download: Not found")
            return None
        elif url[0] == "/":
            url = root+url
        print(url)
        res = requests.get(url,headers=self.headers,cookies=self.jar)
        content_type = res.headers['content-Type']
        if "pdf" not in content_type:
            if depth < 1:
                return self.html_to_pdf(res.content,root,depth=1) #try again, some pages go to a redirect link
            else:
                print("Not pdf",content_type)
                return None
        return res.content




if __name__ == "__main__":
    c = Crawler()
    #c.query("hpc")
    #c.download()
