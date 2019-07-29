from html.parser import HTMLParser

class LinkParser(HTMLParser):
    def handle_starttag(self,tag,attr):
        self.link = attr[0][1]

class PDFFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.pdflist = set()

    def handle_starttag(self, tag, attr):
        self.tag = tag
        self.attr = attr
        url = False
        pdf = False
        if tag == "a":
            for name,val in attr:
                if name == "href":
                    url = val
                    if ".pdf" == val.lower()[-4:]:
                        self.pdflist.add(url)
                        return
                if name == "title" and "pdf" in val.lower():
                    pdf = True
            if url and pdf:
                self.pdflist.add(url)
        elif tag == 'iframe':
            for name,val in attr:
                if name == "src":# and ".pdf" in val.lower():
                    self.pdflist.add(val)


    def handle_data(self,data):
        pass
        #if "pdf" == data.lower()[:3] and self.tag == "a":
        #    self.pdflist.append(self.attr[0][1])
