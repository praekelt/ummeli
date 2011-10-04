from celery.task import task
from celery.task.sets import TaskSet
from ummeli.vlive.jobs.parser import PageParser

class CategoryParser(PageParser):
    def __init__(self,  id,  url = None,  html_str = None):
        self.id = id
        if url:
            self.url = url
            super(CategoryParser,  self).__init__(url = url % {'path': '',  'id': id})
        else:
            super(CategoryParser,  self).__init__(html_str = html_str)
        
    def parse(self):
        links = self.doc.xpath('.//n:tr/*/n:a', namespaces={'n':'http://www.w3.org/1999/xhtml'})
        list = [
                (self.url % {'path': '/' + ''.join(link.xpath('./@href')),  'id': self.id}, 
                ''.join(link.xpath('./*/text()', 
                           namespaces={'n':'http://www.w3.org/1999/xhtml'})))
                for link in links]
        return list
                
class JobsParser(PageParser):
    def parse(self):
        rows = self.doc.xpath('.//n:tr', namespaces={'n':'http://www.w3.org/1999/xhtml'})
        list = []
        for row in rows:
            fonts = row.xpath('.//n:font', namespaces={'n':'http://www.w3.org/1999/xhtml'})
            if len(fonts) == 3:
                data = [' '.join(d.xpath('./text()')) for d in fonts]
                list.append(data)    
        print'----------------- # -------------------'
        return list
