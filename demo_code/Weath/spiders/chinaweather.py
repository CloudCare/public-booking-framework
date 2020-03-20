# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Weath.items import WeathItem
import datetime


def parse_item(response):
    item = WeathItem()

    main_city = "|".join(response.xpath("//div[@class='crumbs fl']//a/text()").extract())
    if main_city == "":
        return None
    suffix_info = response.xpath("//div[@class='crumbs fl']/span[last()]/text()").extract()
    if len(suffix_info):
        main_city += "|"
        main_city += suffix_info[0]
    item["city"] = main_city.replace("全国|", "")

    item["year"] = datetime.datetime.now().year
    item["month"] = datetime.datetime.now().month
    item["day"] = datetime.datetime.now().day

    item["max_temper"] = response.xpath(
        "//div[@class='today clearfix']//ul[@class='clearfix']/li[1]//p[@class='tem']/span/text()").extract()[0]
    item["dt_windlevel"] = response.xpath(
        "//div[@class='today clearfix']//ul[@class='clearfix']/li[1]//p[@class='win']/span/text()").extract()[0]
    item["dt_winddirect"] = response.xpath(
        "//div[@class='today clearfix']//ul[@class='clearfix']/li[1]//p[@class='win']/span/@title").extract()[0]
    item["sunrise_time"] = response.xpath("//div[@class='today clearfix']//ul[@class='clearfix']/li[1]//p[@class='sun sunUp']/span/text()").extract()[0].split()[1]

    item["min_temper"] = response.xpath(
        "//div[@class='today clearfix']//ul[@class='clearfix']/li[2]//p[@class='tem']/span/text()").extract()[0]
    item["nt_windlevel"] = response.xpath(
        "//div[@class='today clearfix']//ul[@class='clearfix']/li[2]//p[@class='win']/span/text()").extract()[0]
    item["nt_winddirect"] = response.xpath(
        "//div[@class='today clearfix']//ul[@class='clearfix']/li[2]//p[@class='win']/span/@title").extract()[0]
    item["sunset_time"] = response.xpath(
        "//div[@class='today clearfix']//ul[@class='clearfix']/li[2]//p[@class='sun sunDown']/span/text()").extract()[0].split()[1]
    return item




class ChinaweatherSpider(CrawlSpider):
    name = 'chinaweather'
    allowed_domains = ['weather.com.cn']
    start_urls = ['http://www.weather.com.cn']

    rules = (
        Rule(LinkExtractor(allow=r'http://www.weather.com.cn/weather1d/\d{9}.shtml'), callback= parse_item, follow=True),
    )



