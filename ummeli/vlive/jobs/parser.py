import urllib
import StringIO
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

        self.url = url
        self.html_str = html_str

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
        s = str(s).replace('<br />', '').replace('\n', '').replace('&', '&amp;')
        return s

    def get_document(self):
        if self.url:
            return etree.parse(StringIO.StringIO(self.get_html(self.url)))
        elif self.html_str:
            return etree.parse(StringIO.StringIO(self.tidy_html(self.html_str)))

        raise Exception('Parameters invalid', 'Url or html_str required.')
