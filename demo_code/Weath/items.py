# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeathItem(scrapy.Item):
    city = scrapy.Field()  # 城市信息：“江苏|苏州|太仓” 或者景点信息 “江苏|常熟|沙家浜风景区”

    year  = scrapy.Field()   # 年
    month = scrapy.Field()   # 月
    day   = scrapy.Field()   # 日

    dt_winddirect = scrapy.Field()  # 白天风向
    dt_windlevel  = scrapy.Field()  # 白天风力
    max_temper    = scrapy.Field()  # 白天最高温度
    sunrise_time  = scrapy.Field()  # 日出时间

    nt_winddirect = scrapy.Field()  # 夜间风向
    nt_windlevel  = scrapy.Field()  # 夜间风力
    min_temper    = scrapy.Field()  # 夜晚最低温度
    sunset_time   = scrapy.Field()  # 日落时间

