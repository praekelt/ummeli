from celery.task import task
from celery.task.sets import TaskSet
from ummeli.vlive.jobs.parser import PageParser

class CategoryParser(PageParser):
    def __init__(self,  search_id,  url = None,  html_str = None):
        self.search_id = search_id
        if url:
            self.raw_url = url
            super(CategoryParser,  self).__init__(url = url % {'path': '',  'id': search_id})
        else:
            super(CategoryParser,  self).__init__(html_str = html_str)
            
    def parse(self):
        doc = self.get_document()
        links = doc.xpath('.//n:tr/*/n:a', namespaces={'n':'http://www.w3.org/1999/xhtml'})
        
        list = [
                (self.raw_url % {'path': '/' + ''.join(link.xpath('./@href')),  'id': self.search_id}, 
                ''.join(link.xpath('./*/text()')))
                for link in links]
        return list
                
class JobsParser(PageParser):
    def parse(self):
        doc = self.get_document()
        rows = doc.xpath('.//n:tr', namespaces={'n':'http://www.w3.org/1999/xhtml'})
        list = []
        for row in rows:
            fonts = row.xpath('.//n:font', namespaces={'n':'http://www.w3.org/1999/xhtml'})
            if len(fonts) == 3:
                data = [(' '.join(d.xpath('./text()'))).encode('ascii', 'ignore') for d in fonts]
                list.append(data)
        return list
