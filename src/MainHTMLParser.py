from html.parser import HTMLParser
class mainHTTPParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.lessons=[]
        self.node=[]
        self.flag=-1
        '''
        flag
        1:课程名称
        2：作业
        3：公告
        4：文件'''
    def handle_starttag(self, tag, attrs):
        if(tag=='tr' and self.flag==-1):
            for (key,value) in attrs:
                if(key=='class' and (value=='info_tr2' or value =='info_tr')):
                    self.flag=0
        if(tag=='tr' and self.flag > 0):
            self.node.append('0')
            self.node.append('0')
            self.node.append('0')
            self.lessons.append(self.node)
            self.node=[]
            for (key,value) in attrs:
                if(key=='class' and (value=='info_tr2' or value =='info_tr')):
                    self.flag=0
        if(tag=='a' and self.flag == 0):
            self.flag = 1
            str = attrs[0][1]
            pos = str.find('id=')+3
            if(pos == -1):
                pos = str.find('home')+5
            lens = len(str)
            self.node.append(str[pos:lens])
        elif(self.flag==1 and tag == 'span'):
            for (key,value) in attrs:
                if(key=='class' and value == 'red_text'):
                    self.flag=2
        elif(self.flag==2 and tag == 'span'):
            for (key,value) in attrs:
                if(key=='class' and value == 'red_text'):
                    self.flag=3
        elif(self.flag==3 and tag == 'span'):
            for (key,value) in attrs:
                if(key=='class' and value == 'red_text'):
                    self.flag=4
    def handle_data(self, data):
        if(self.flag==1 and len(data)>10):
            strend = data.index('(2017')
            self.node.append(data[10:strend])
        if(self.flag==2 and len(data)<4):
            self.node.append(data)
        if(self.flag==3 and len(data)<4):
            self.node.append(data)
        if(self.flag==4 and len(data)<4):
            self.node.append(data)
            self.flag = -1
            self.lessons.append(self.node)
            self.node=[]
