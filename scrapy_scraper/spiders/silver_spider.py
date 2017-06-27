import scrapy
from scrapy_scraper.settings import SPIDER_URL, CUSTOM_SILVER_URL
from scrapy_scraper.items import ModelItem
from scrapy import Request
import logging
import re

class SilverSpider(scrapy.Spider):
    name = "silver"

    start_urls = [SPIDER_URL[name]]

    def parse(self, response):
        # follow links to author pages
        for href in response.css('div.acompanhante a::attr(href)'):
            yield response.follow(href, self.parse_model)

    def parse_photos(self, reponse):
        logging.info(re.findall(r'\w*(?<=[0-9]).jpg/ensaios', response.body))

    def get_photos(self, response):
        model_id = response.xpath('//div[@class="ensaio"]/a/@data-source').extract_first()
        url = CUSTOM_SILVER_URL + model_id
        res =  Request(url)
        logging.info(res.body)

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

        def extract_links():
            # return re.findall(r'\w*(?<=[0-9]).jpg/ensaios', response.body)
            return response.xpath('//div[@class="ensaio-destaque"]/img[1]/@src').extract_first()

        item = ModelItem()
        item['name'] = extract_with_css('div.info-white h1::text')
        item['phone'] = extract_with_css('div.info-white p.telefone::text')
        item['photoLinks'] = extract_links()
        # 'profile': {
        #     'age': extract_with_xpath('//div[@class="item"][1]//span/following-sibling::text()[1]'),
        #     'height': extract_with_xpath('//div[@class="item"][2]//span/following-sibling::text()[1]'),
        #     'weight': extract_with_xpath('//div[@class="item"][3]//span/following-sibling::text()[1]'),
        #     'hair': extract_with_xpath('//div[@class="item"][7]//span/following-sibling::text()[1]'),
        #     },
        yield item

# este tem que ter mais niveis para fazer scrape de cidades diferentes
