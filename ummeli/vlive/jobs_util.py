import urllib
from xml.dom.ext.reader import HtmlLib
from xml.dom import Document
from tidylib import tidy_document as tidy
from django.core.cache import cache

def get_document(url):
    usock = urllib.urlopen(url)
    html_str = usock.read()
    usock.close()
    
    reader = HtmlLib.Reader()
    s, err = tidy(html_str,  options={'output-xhtml': False,
                                                        'doctype': 'omit', 
                                                        'numeric-entities':1})
                                                        
    return reader.fromString(str(s))
    
def get_links(url,  id):
    jobs_url = url % {'id': id,  'path':''}    
    print jobs_url
    
    doc = get_document(jobs_url)
    
    table_elements = doc.getElementsByTagName("table")
    a_elements = [v.getElementsByTagName('a')[0] for v in table_elements if v.getElementsByTagName('a')[0] .attributes.length == 1]
    list = [(a.firstChild.firstChild.nodeValue, url % {'id': id,  'path': '/' + a.attributes.item(0).value}) for a in a_elements]
    return list
    
def get_jobs(url):
    print url
    
    doc = get_document(url)
    row_elements = doc.getElementsByTagName("tr")
    font_elements = [(v.getElementsByTagName('font')[0],  
                                v.getElementsByTagName('font')[1],  
                                ''.join([get_text(a) for a in v.getElementsByTagName('font')[2].childNodes ])) for v in row_elements if v.getElementsByTagName('font').length == 3]
                                
    list = [(font[0].firstChild.nodeValue, font[1].lastChild.nodeValue,  font[2]) for font in font_elements]
    return list

def get_text(node):
    if('Text Node' in str(node)):
        return node.nodeValue
    return ''
