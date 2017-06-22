import scrapy
from scrapy_scraper.settings import SPIDER_URL

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
            return response.css(query).extract_first().strip()

        def extract_all_with_xpath(query):
            return response.xpath(query).extract()

        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        def extract_profile_with_xpath(query):
            keys = ['age', 'height', 'weight']
            profile = {}
            profile_items = response.xpath(query).extract()
            for key, item in zip(keys, profile_items):
                profile[key] = item.strip(' ')
            return profile

        yield {
            'name': extract_with_css('div.info-white h1::text'),
            'phone': extract_with_css('div.info-white p.telefone::text'), #.re(((apenas numeros)))
            'place': extract_with_css('div.local h3::text').strip('Local: '),
            'profile': extract_profile_with_xpath('//div[@class="info"]/span/following-sibling::text()'),
            'photo-links': extract_all_with_xpath('//div[@class="foto"]/a/@href')
        }

# este tem que ter mais niveis para fazer scrape de cidades diferentes
