import scrapy
from scrapy_scraper.settings import SPIDER_URL

class YellowSpider(scrapy.Spider):
    name = "yellow"

    start_urls = [SPIDER_URL[name]]

    def parse(self, response):
        # follow links to author pages
        for href in response.css('div.anuncio a::attr(href)'):
            print(href)
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

        yield {
            'name': extract_with_xpath('//span[@id="anuncio-nombre"]::text()[1]'),
            # 'phone': extract_with_css('p.fone strong::text'), #.re(((apenas numeros)))
            # 'place': extract_with_css('div.local h3::text').strip('Local: '),
            # 'profile': extract_profile_with_xpath('//div[@class="infos"]/div[@class="col3"][1]/p/strong/following-sibling::text()[1]'),
            # 'photo-links': extract_all_with_xpath('//div[@class="cycle-slideshow"]/a/@href')
        }
