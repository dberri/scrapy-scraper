import scrapy
from scrapy_scraper.settings import SPIDER_URL
import logging
import re

class SilverSpider(scrapy.Spider):
    name = "silver"

    start_urls = [SPIDER_URL[name]]

    def parse(self, response):
        # follow links to author pages
        for href in response.css('div.acompanhante a::attr(href)'):
            yield response.follow(href, self.parse_model)

        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

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
            logging.info(re.findall(r'\w*(?<=[0-9]).jpg/ensaios', response.body))

        yield {
            'name': extract_with_css('div.info-white h1::text'),
            'phone': extract_with_css('div.info-white p.telefone::text'),
            # 'place': extract_with_css('div.local h3::text').strip('Local: '),
            'profile': {
                'age': extract_with_xpath('//div[@class="item"][1]//span/following-sibling::text()[1]'),
                'height': extract_with_xpath('//div[@class="item"][2]//span/following-sibling::text()[1]'),
                'weight': extract_with_xpath('//div[@class="item"][3]//span/following-sibling::text()[1]'),
                'hair': extract_with_xpath('//div[@class="item"][7]//span/following-sibling::text()[1]'),
                },
            'photo-links': extract_links()
            # 'photo-links': extract_all_with_xpath('//a/img/@src')
        }

# este tem que ter mais niveis para fazer scrape de cidades diferentes
