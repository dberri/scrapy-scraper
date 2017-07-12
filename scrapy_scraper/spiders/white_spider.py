import scrapy
from scrapy_scraper.settings import SPIDER_URL
from scrapy_scraper.items import ModelItem

class WhiteSpider(scrapy.Spider):
    name = "white"

    start_urls = [SPIDER_URL[name]]

    def parse(self, response):
        # follow links to author pages
        for href in response.css('a.thumb-info::attr(href)'):
            yield response.follow(href, self.parse_model)


    def parse_model(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        def extract_all_with_xpath(query):
            return response.xpath(query).extract()

        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        # def extract_profile_with_xpath(query):
        #     keys = ['age', 'type', 'biotype', 'height', 'weight', 'manequim', 'feet', 'hair', 'eyes']
        #     profile = {}
        #     profile_items = response.xpath(query).extract()
        #     for key, item in zip(keys, profile_items):
        #         profile[key] = item.strip(' ')
        #     return profile

        name = extract_with_xpath('//strong/span[@itemprop="name"]::text()')
        item = ModelItem()
        item['name'] = name
        # item['phone'] = extract_with_css('p.telefone-modelo-interna::text')
        item['photoLinks'] = extract_all_with_xpath('//div[@class="col-xs-12"]/img[contains(@src, "gatas")]/@src')
        # 'city': extract_with_css('p.cidade-modelo::text')
        # 'profile': extract_profile_with_xpath('//li[@class="opcao-submenu"]/span[1]/following-sibling::text()[1]')
        yield item
