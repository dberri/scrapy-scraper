import scrapy
from scrapy_scraper.settings import SPIDER_URL
from scrapy_scraper.items import ModelItem
import logging

class BlackSpider(scrapy.Spider):
    name = "brown"

    start_urls = [SPIDER_URL[name]]

    def parse(self, response):
        # follow links to author pages
        for href in response.css('article > a::attr(href)'):
            yield response.follow(href, self.parse_model)


    def parse_model(self, response):

        def extract_all_with_xpath(query):
            return response.xpath(query).extract()

        def extract_with_xpath(query):
            logging.info(response.url)
            return response.xpath(query).extract_first().strip()

        def extract_phone():
            result = response.xpath('//span[@itemprop="telephone"]/a/text()').extract_first()
            if result is not None:
                return result.strip()

            elif response.xpath('//a[contain(@href,"tel")/text()').extract_first():
                return response.xpath('//a[contain(@href,"telephone")/text()').extract_first().strip()

            else:
                logging.warning('No phone extracted!')



        item = ModelItem()
        item['name'] = extract_with_xpath('//span[@itemprop="name"]/text()')
        item['phone'] = extract_phone()
        logging.info(item['phone'])
        # item['photoLinks'] = extract_all_with_xpath('//figure/a/@href')
        # 'city': extract_with_css('p.cidade-modelo::text')
        # 'profile': extract_profile_with_xpath('//li[@class="opcao-submenu"]/span[1]/following-sibling::text()[1]')
        yield item
