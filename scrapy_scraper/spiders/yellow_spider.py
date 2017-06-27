import scrapy
from scrapy_scraper.settings import SPIDER_URL
from scrapy_scraper.items import ModelItem
import logging

class YellowSpider(scrapy.Spider):
    name = "yellow"

    start_urls = [SPIDER_URL[name]]

    def parse(self, response):
        yield scrapy.FormRequest.from_response(response=response, callback=self.parse_page)

    def parse_page(self, response):
        # follow links to author pages
        for href in response.css('div.anuncio a::attr(href)'):
            print(href)
            yield response.follow(href, self.parse_model)

    def parse_model(self, response):
        def extract_with_css(query):
            result = response.css(query).extract_first()
            if result is not None:
                return result.strip()
            else:
                logging.warning(response.url)

        def extract_all_with_xpath(query):
            return response.xpath(query).extract()

        def extract_with_xpath(query):
            result = response.xpath(query).extract_first()
            if result is not None:
                return result.strip()
            else:
                logging.warning(response.url)

        def extract_profile_with_xpath(query):
            keys = ['age', 'height', 'weight', 'manequim']
            profile = {}
            profile_items = response.xpath(query).extract()
            for key, item in zip(keys, profile_items):
                profile[key] = item.strip()
            return profile

        item = ModelItem()
        item['name'] = extract_with_xpath('//span[@id="anuncio-nombre"]/text()[1]')
        item['phone'] = extract_with_css('span.telephone::text')
        # item['photoLinks'] =
        # 'place': extract_with_xpath('//span[@id="anuncio-poblacion"]/text()[1]'),

        yield item
