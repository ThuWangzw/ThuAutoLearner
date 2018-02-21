from html.parser import HTMLParser
class newDetailParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.detail=""
    def handle_data(self, data):
        self.detail=self.detail+data
