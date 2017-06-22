# -*- coding: utf-8 -*-
import scrapy
from scrapy_scraper.settings import SPIDER_URL
import logging

class PinkSpider(scrapy.Spider):
    name = "pink"

    start_urls = [SPIDER_URL[name]]

    def parse(self, response):
        # follow links to model pages
        for href in response.css('a.uk-thumbnail::attr(href)').extract():
            yield response.follow(href, self.parse_model)

    def parse_model(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        def extract_all_with_xpath(query):
            return response.xpath(query).extract()

        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        def extract_profile_with_xpath(query):
            keys = ['hair', 'age', 'height', 'weight']
            profile = {}
            profile_items = response.xpath(query).extract_first().strip()
            # for key, item in zip(keys, profile_items):
            #     profile[key] = item.strip()
            return profile_items
            # iterate and find item by item with regex

        yield {
            'name': extract_with_css('h5.uk-margin-top-remove::text'),
            'phone': extract_with_xpath('//tbody/tr[3]/td[2]/text()'),
            'city': extract_with_xpath('//tbody/tr[1]/td[2]/text()'),
            'profile': extract_profile_with_xpath('//caption/text()'),
            'photo-links': extract_all_with_xpath('//div[@class="slides-container"]/ul/li/img/@data-src') # Não pega o primeiro link que vem de img src
        }

# sera necessario mais niveis de scraping
