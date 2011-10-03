from ummeli.vlive.jobs.parser import PageParser

class CategoryParser(PageParser):
    def __init__(self,  url = None,  html_str = None):
        if url:
            self.url = url
            super(CategoryParser,  self).__init__(url = url % {'path': ''})
        else:
            super(CategoryParser,  self).__init__(html_str = html_str)
        
    def parse(self):
        links = self.doc.xpath('.//n:tr/*/n:a', namespaces={'n':'http://www.w3.org/1999/xhtml'})
        
        return [
                (self.url % ('/' + ''.join(link.xpath('./@href'))), 
                ''.join(link.xpath('./*/text()', 
                           namespaces={'n':'http://www.w3.org/1999/xhtml'})))
                for link in links]
                
class JobsParser(PageParser):
    def parse(self):
        rows = self.doc.xpath('.//n:tr', namespaces={'n':'http://www.w3.org/1999/xhtml'})
        list = []
        for row in rows:
            fonts = row.xpath('.//n:font', namespaces={'n':'http://www.w3.org/1999/xhtml'})
            if len(fonts) == 3:
                data = [''.join(d.xpath('./text()')) for d in fonts]
                list.append(data)    
        return list
    
def get_links(url):
    processor = CategoryParser(url = url)
    return processor.parse()
    
def get_jobs(url):
    processor = JobsParser(url = url)
    return processor.parse()

def update_jobs_db():
    # for(1,2,5,6)
        #get cat (5 seconds delay) - CategoryParser
            #get jobs(10 seconds delay) - JobsParser
    #ETA: (5*4 =20s) + (40*4*10 = 1600s) = +-30mins
    return []
