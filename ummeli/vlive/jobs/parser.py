import urllib,  StringIO
from tidylib import tidy_document as tidy
from lxml import etree

class PageParser(object):
    """Uses self.doc to parse the document tree, preferable using xpath
    e.g self.doc.xpath('.//tr')
    """
    def parse(self):
        raise NotImplementedError( "Should have implemented this" )
    
    def __init__(self,  url = None,  html_str = None):
        if(url and html_str):
            raise Exception('Parameters invalid', 'Only 1 parameter required.')
            
        if url:
            self.doc = self.get_document(self.get_html(url))
        elif html_str:
            self.doc = self.get_document(self.tidy_html(html_str))
        else:
            raise Exception('Parameters invalid', 'Url or html_str required.')
        
    def get_html(self,  url):
        usock = urllib.urlopen(url)
        html_str = usock.read()
        usock.close()
        
        return self.tidy_html(html_str)
        
    def tidy_html(self,  html_str):
        s, err = tidy(html_str,  options={'output-xhtml': True,
                                                            'doctype': 'omit', 
                                                            'numeric-entities':1, 
                                                            'bare': True, 
                                                            'indent': False})
        s = str(s).replace('<br />', '').replace('\n', '')
        return s
        
    def get_document(self, html):        
        return etree.parse(StringIO.StringIO(html))
