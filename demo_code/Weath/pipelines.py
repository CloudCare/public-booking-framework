# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import nsq
import json
import urllib
import pymysql


class WeathPipelineUnique(object):
    def __init__(self):
        self.has_seen = set()

    def process_item(self, item, spider):
        city = item["city"]
        if city in self.has_seen:
            raise DropItem("Duplicate book found:%s" % item)
        self.has_seen.add(city)
        return item

class MySqlPipeline(object):
    def __init__(self, host, port, user, passwd, database):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.con = None
        self.cur = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = crawler.settings.get('MYSQL_HOST', "127.0.0.1"),
            port = crawler.settings.get('MYSQL_PORT', 3306),
            user = crawler.settings.get('MYSQL_USER', "test"),
            passwd = crawler.settings.get('MYSQL_PASSWD', "123456"),
            database = crawler.settings.get('MYSQL_DATABASE', "weather"),
        )

    def open_spider(self, spider):
        self.con = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.passwd,
                                   db=self.database, charset='utf8')
        self.cur = self.con.cursor()

    def process_item(self, item, spider):
        data = dict(item)
        if self.cur:
            sql = """Insert into china_weather(city, year, month, day, dt_winddirect, dt_windlevel, max_temper, sunrise_time, nt_winddirect, nt_windlevel  ,min_temper, sunset_time )
            values('%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s', '%s')""" %(data["city"], data["year"], data["month"], data["day"], data["dt_winddirect"], data["dt_windlevel"], data["max_temper"], data["sunrise_time"], data["nt_winddirect"], data["nt_windlevel"], data["min_temper"], data["sunset_time"] )
            self.cur.execute(sql)
            self.con.commit()
        return item


    def close_spider(self, spider):
        if self.cur:
            self.cur.close()
        if self.con:
            self.con.close()


class JsonFilePipeline(object):
    def __init__(self, json_file_name):
        self.json_file_name = json_file_name
        self.json_file      = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            json_file_name =crawler.settings.get('JSON_FILE_NAME', None),
        )

    def open_spider(self, spider):
        if self.json_file_name and self.json_file_name != "":
            self.json_file = open(self.json_file_name, "a")

    def process_item(self, item, spider):
        if self.json_file:
            # self.json_file.write(json.dumps(dict(item), ensure_ascii=False))
            json.dump(dict(item), fp=self.json_file, ensure_ascii=False)
        return item

    def close_spider(self, spider):
        if self.json_file:
            self.json_file.close()

class NsqHttpPipeline(object):
    def __init__(self, http_url):
        self.http_url = http_url
        self.headers = {'Content-Type': 'application/json'}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            http_url=crawler.settings.get('HTTP_URI', None),
        )

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if self.http_url:
            request = urllib.request.Request(url=self.http_url, headers=self.headers,
                                             data=json.dumps(dict(item), ensure_ascii=False).encode(encoding='UTF8'))
            response = urllib.request.urlopen(request)  # 发送请求

            status_code  = response.read().decode()
        return item

    def close_spider(self, spider):
        pass


class NsqPipeline(object):
    def __init__(self, nsq_url):
        self.nsq_url = nsq_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            nsq_url=crawler.settings.get('NSQ_URI'),
        )

    def open_spider(self, spider):
        self.writer = nsq.Writer([self.nsq_url])
        nsq.run()

    def process_item(self, item, spider):
        jstr = json.dumps(dict(item), ensure_ascii=False)
        self.writer.pub("weather_info", jstr, self.finish_pub_cb)
        return item

    def close_spider(self, spider):
        pass

    def finish_pub_cb(self, conn, data):
        pass
