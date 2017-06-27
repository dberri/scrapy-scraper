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
        for href in response.xpath('//div[@id="resultados"]/div/div/a[1]/@href'):
            yield response.follow(href, self.parse_model)

    def parse_model(self, response):
        def extract_all_with_xpath(query):
            return response.xpath(query).extract()

        def extract_with_xpath(query):
            result = response.xpath(query).extract_first()
            if result is not None:
                return result.strip()
            else:
                logging.warning(response.url)

        item = ModelItem()
        item['name'] = extract_with_xpath('//span[@id="anuncio_nombre"]/text()')
        item['phone'] = extract_with_xpath('//span[@itemprop="telephone"]/text()')
        item['photoLinks'] = extract_all_with_xpath('//div[@id="anuncio_fotos"]//img/@src')
        # 'place': extract_with_xpath('//span[@id="anuncio-poblacion"]/text()[1]'),
        yield item

# implement check if isn't in the database
