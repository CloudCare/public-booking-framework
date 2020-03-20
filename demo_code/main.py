from scrapy import cmdline

cmdline.execute("scrapy crawl chinaweather -o china_weather.csv".split())