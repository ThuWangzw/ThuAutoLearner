from html.parser import HTMLParser
class hwListHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag=-1
        self.hw=[]
        self.node=[]
    def handle_starttag(self, tag, attrs):
        if(tag=='tr'):
            for (key,value) in attrs:
                if(key=='class' and (value == 'tr1' or value == 'tr2')):
                    self.flag=0
        elif(tag=='a' and self.flag == 0):
            for (key,value) in attrs:
                if(key=='href'):
                    self.node.append('http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/'+value)
            self.flag=1
    def handle_data(self, data):
        if(self.flag == 1 and len(data) > 1):
            data = data.replace(u'\xa0',u' ')
            self.node.append(data)
            self.flag = 2
        elif(self.flag==2 and len(data)>1):
            self.flag=3
        elif(self.flag==3 and len(data)>1):
            self.flag = 4
            self.node.append(data)
        elif(self.flag==4 and len(data)>1):
            self.flag = 5
        elif(self.flag==5 and len(data)>1):
            self.flag = 6
            self.node.append(data)
        elif(self.flag==6 and len(data)>1):
            self.flag = 7
        elif(self.flag==7 and len(data)>1):
            data = data.replace(u'\xa0',u'')
            data = data.replace(u'\r',u'')
            data = data.replace(u'\n',u'')
            data = data.replace(u'\t',u'')
            data = data.replace(u' ',u'')
            self.node.append(data)
            self.hw.append(self.node)
            self.node = []
            self.flag=-1
