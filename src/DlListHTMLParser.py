from html.parser import HTMLParser
class dlListHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag=-1
        self.dl=[]
        self.node=[]
    def handle_starttag(self, tag, attrs):
        if(tag == 'tr'):
            for (key,value) in attrs:
                if(key=='class' and (value == 'tr1' or value == 'tr2')):
                    self.flag=0
        if(self.flag == 0 and tag == 'a'):
            for (key,value) in attrs:
                if(key=='href'):
                    self.node.append('http://learn.tsinghua.edu.cn' + value)
            self.flag = 1
        if(self.flag>1 and tag == 'td'):
            self.flag = self.flag + 1
    def handle_data(self, data):
        if(self.flag==1):
            data = data.replace(u'\xa0','')
            data = data.replace('\r','')
            data = data.replace('\n','')
            data = data.replace('\t','')
            data = data.replace(' ','')
            if(data != ''):
                self.node.append(data)
                self.flag = self.flag+1
        if(self.flag > 1 and self.flag%2 == 1):
            data = data.replace(u'\xa0','')
            data = data.replace('\r','')
            data = data.replace('\n','')
            data = data.replace('\t','')
            data = data.replace(' ','')
            self.node.append(data)
            self.flag = self.flag+1
            if(self.flag==10):
                self.flag = -1
                self.dl.append(self.node)
                self.node = []
