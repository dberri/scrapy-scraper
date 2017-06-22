import scrapy
from scrapy_scraper.settings import SPIDER_URL

class BlackSpider(scrapy.Spider):
    name = "black"

    start_urls = [SPIDER_URL[name]]

    def parse(self, response):
        # follow links to author pages
        for href in response.css('ul.lista-modelos li a::attr(href)'):
            yield response.follow(href, self.parse_model)


    def parse_model(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        def extract_all_with_xpath(query):
            return response.xpath(query).extract()

        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        def extract_profile_with_xpath(query):
            keys = ['age', 'type', 'biotype', 'height', 'weight', 'manequim', 'feet', 'hair', 'eyes']
            profile = {}
            profile_items = response.xpath(query).extract()
            for key, item in zip(keys, profile_items):
                profile[key] = item.strip(' ')
            return profile

        yield {
            'first_name': extract_with_css('p.nome-modelo-interna span.color::text'),
            'last_name': extract_with_xpath('//p[@class="nome-modelo-interna"]/span[1]/following-sibling::text()[1]'),
            'phone': extract_with_css('p.telefone-modelo-interna::text'),
            'city': extract_with_css('p.cidade-modelo::text'),
            'profile': extract_profile_with_xpath('//li[@class="opcao-submenu"]/span[1]/following-sibling::text()[1]'),
            'photo-links': extract_all_with_xpath('//li/img[contains(@src, "modelos")]/@src')
        }
