import scrapy
import re
from urlparse import urlparse 

class RTMPLink(scrapy.Item):
    link = scrapy.Field()
    from_url = scrapy.Field()

class RTMPCrawlerSpider(scrapy.Spider):
    name = 'rtmp_crawler'
    start_url = 'http://www.glaz.tv'
    rtmp_link_pattern = re.compile('rtmp://[A-Za-z0-9:/?%#.\-_]*')
    file_link_pattern = re.compile('file=[A-Za-z0-9:/?%#.\-_]*')

    links = set()
    filter_dictionary = set()
    filter_links = urlparse(start_url).netloc
    def parse(self, response):
        sel = scrapy.Selector(response=response)

        for rtmp in sel.re(self.rtmp_link_pattern):
            yield RTMPLink(link=rtmp, from_url=response.url)
        for file_link in sel.re(self.file_link_pattern):
            yield RTMPLink(link=file_link, from_url=response.url)
        for url in response.xpath('//a/@href').extract():
            # print url
            created = False
            if url[0] == '/':
                url = self.start_url + url.strip()
                created = True
                # print "Parsed url" + url
            isOk = True
            
            if not created:
                web_link = urlparse(url).netloc
                if not web_link == self.filter_links:
                    isOk = False

            if url in self.links:
                isOk = False

            if isOk:
                self.links.add(url)
                yield scrapy.Request(url, callback=self.parse)
                
