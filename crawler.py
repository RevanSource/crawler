import scrapy
import re
from urlparse import urlparse 

class RTMPLink(scrapy.Item):
    link = scrapy.Field()
    from_url = scrapy.Field()

class RTMPCrawlerSpider(scrapy.Spider):
    name = 'rtmp_crawler'
    start_urls = ['http://www.glaz.tv']
    rtmp_link_pattern = re.compile('rtmp://[a-z0-9:/?%#.]*')
    links = set()
    filter_dictionary = set()
    filter_links = urlparse(start_urls[0]).netloc
    def parse(self, response):
        # for rtmp in response.xpath('//a[contains(@href, "rtmp")]/@href').extract():
        sel = scrapy.Selector(response=response)

        for rtmp in sel.re(self.rtmp_link_pattern):
            yield RTMPLink(link=rtmp, from_url=response.url)

        for url in response.xpath('//a/@href').extract():
            # print url
            created = False
            if url[0] == '/':
                url = self.start_urls[0] + url.strip()
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
                
