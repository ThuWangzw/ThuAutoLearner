from html.parser import HTMLParser
class hwHTTPParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag=-1
        self.text=''
        self.url = ''
        self.havefile=1
    def handle_starttag(self, tag, attrs):
        if(tag == 'textarea' and self.flag==-1):
            self.flag=0
        if(self.flag==2 and tag == 'td'):
            self.flag=3
        if(self.flag==5 and tag == "a"):
            for (key,value) in attrs:
                if(key=='href'):
                    self.url = 'http://learn.tsinghua.edu.cn'+value
                    self.flag = -2
    def handle_data(self, data):
        if(self.flag == 0):
            self.flag = 1
            data = data.replace(u'\xa0',u'')
            data = data.replace(u'\r',u'')
            data = data.replace(u'\n',u'')
            data = data.replace(u'\t',u'')
            data = data.replace(u' ',u'')
            self.text = data
        elif(data==' 作业附件'):
            self.flag=2
        elif(self.flag==3):
            data = data.replace(u'\xa0','')
            data = data.replace('\r','')
            data = data.replace('\n','')
            data = data.replace('\t','')
            data = data.replace(' ','')
            if('无相关文件' in data):
                self.havefile = 0
                self.flag = -2
            else:
                self.flag = 5
