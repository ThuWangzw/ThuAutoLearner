from html.parser import HTMLParser
class noteHTTPParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag=-1
        self.text=''
    def handle_data(self, data):
        if(data=='正文'):
            self.flag=0
        elif(self.flag==0 and len(data)>1):
            self.flag=1
        elif(self.flag==1):
            self.text=data
            self.text.replace('\xa0 ', ' ')
            self.flag=2
