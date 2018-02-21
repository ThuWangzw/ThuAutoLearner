from html.parser import HTMLParser
class noteListHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.note=[]
        self.node=[]
        self.flag=-1
    def handle_starttag(self, tag, attrs):
        if(tag=='tr'):
            for (key,value) in attrs:
                if(key=='class' and (value == 'tr1' or value == 'tr2')):
                    self.flag=0
        elif(self.flag==2):
            for (key,value) in attrs:
                if(key=='href'):
                    self.flag=3
                    self.node.append('http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/'+value)
        elif(self.flag==3 and tag == 'td'):
            self.flag=4
        elif(self.flag==4 and tag == 'td'):
            self.flag=5
        elif(self.flag==5 and tag == 'td'):
            self.flag=6
        elif(self.flag==0 or self.flag == 1):
            self.flag=self.flag + 1
    def handle_data(self, data):
        data = data.replace(u'\xa0',u'')
        data = data.replace(u'\r',u'')
        data = data.replace(u'\n',u'')
        data = data.replace(u'\t',u'')
        data = data.replace(u' ',u'')
        if(self.flag==3 and len(data)>1):
            self.node.append(data)
        if(self.flag==4 and len(data)>1):
            self.node.append(data)
        if(self.flag==5 and len(data)>1):
            self.node.append(data)
        if(self.flag==6 and len(data)>1):
            self.node.append(data)
            if(self.node[4] == '已读'):
                self.node[4]=0
            else:
                self.node[4]=1
            self.note.append(self.node)
            self.node=[]
            self.flag=-1
