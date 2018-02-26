from html.parser import HTMLParser
class noteHTTPParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag=-1
        self.text=''
    def handle_data(self, data):
        if(data=='正文'):
            self.flag=1
        elif(self.flag==2):
            data = data.replace(u'\xa0',u'')
            data = data.replace(u'\r',u'')
            data = data.replace(u'\n',u'')
            data = data.replace(u'\t',u'')
            data = data.replace(u' ',u'')
            self.text=self.text+data
    def handle_endtag(self, tag):
        if(tag=="td" and self.flag==1):
            self.flag=2
        elif(tag=="td" and self.flag==2):
            self.flag = -1

