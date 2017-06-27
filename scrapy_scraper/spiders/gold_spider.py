import scrapy
from scrapy_scraper.settings import SPIDER_URL
from scrapy_scraper.items import ModelItem

class GoldSpider(scrapy.Spider):
    name = "gold"

    start_urls = [SPIDER_URL[name]]

    def parse(self, response):
        # follow links to author pages
        for href in response.css('div.inner a::attr(href)'):
            yield response.follow(href, self.parse_model)


    def parse_model(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        def extract_all_with_xpath(query):
            return response.xpath(query).extract()

        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        def extract_profile_with_xpath(query):
            keys = ['age', 'height', 'weight', 'manequim']
            profile = {}
            profile_items = response.xpath(query).extract()
            for key, item in zip(keys, profile_items):
                profile[key] = item.strip(' ')
            return profile

        item = ModelItem()
        item['name'] = extract_with_css('div.titulo h1::text')
        item['phone'] = extract_with_css('p.fone strong::text') #.re(((apenas numeros)))
        item['photoLinks'] = extract_all_with_xpath('//div[@class="cycle-slideshow"]/a/@href')
        # 'place': extract_with_css('div.local h3::text').strip('Local: '),
        # 'profile': extract_profile_with_xpath('//div[@class="infos"]/div[@class="col3"][1]/p/strong/following-sibling::text()[1]')
        yield item
