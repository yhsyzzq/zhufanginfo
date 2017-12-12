import scrapy, re
from datetime import datetime
from datetime import timedelta


class Zhufang58Spider(scrapy.Spider):
    name = 'zhufang58'
    # 减慢爬取速度 为1s
    download_delay = 1
    allowed_domains = ['sh.58.com/', 'jxjump.58.com']
    start_urls = ['http://sh.58.com/chuzu/']

    def parse(self, response):
        sel = scrapy.Selector(response)
        urls = sel.xpath('//ul/li/div[@class="des"]/h2/a/@href').extract()
        i = 0;
        for url in urls:
            if i < 10:
                # print(url)
                yield scrapy.Request(url, callback=self.parse_room)
                i = i + 1

    def parse_room(self, response):
        def response_to_xpath(query):
            return response.xpath(query).extract_first().strip()

        # 标题
        title = response_to_xpath('//div[@class="house-title"]/h1/text()')
        # 发布时间
        publishTime = response_to_xpath('//div[@class="house-title"]/p/text()')
        publishTime = self.formatTime(publishTime)
        # 租金
        price = response_to_xpath('//div[@class="house-pay-way f16"]/span[@class="c_ff552e"]/b/text()')
        # 支付方式
        payType = response_to_xpath('//div[@class="house-pay-way f16"]/span[@class="c_333"]/text()')
        # 租赁方式
        rentType = response_to_xpath('//ul[@class="f14"]/li[1]/span[2]/text()')

        print("标题：" + title)
        print("发布时间：" + publishTime)
        print("租金：" + price)
        print("支付方式：" + payType)
        print("租赁方式：" + rentType, end="\r\n\r\n")

    def formatTime(self, dateStr):
        now = datetime.now()

        reg = '房源编号：(\S*)\xa0\xa0\xa0\xa0\r\n(.*)'
        if re.search(reg, dateStr):
            # print("************************=====================================**************************")
            searchObj = re.search(reg, dateStr)
            # print(searchObj.span())
            # print(searchObj.group())
            # print(searchObj.group(0))
            # print(searchObj.group(1))
            # print(searchObj.group(2))
            # print("************************=====================================**************************")
            dateStr = str(searchObj.group(2)).strip()

        if re.search("小时前", dateStr):
            hoursNum = int(re.sub('小时前', '', dateStr))
            hours = timedelta(hours=hoursNum)
            datetime2 = now - hours
            return datetime2.strftime('%Y-%m-%d %H:%M:%S')
        elif re.search("分钟前", dateStr):
            minitesNum = int(re.sub('分钟前', '', dateStr))
            minites = timedelta(minutes=minitesNum)
            datetime2 = now - minites
            return datetime2.strftime('%Y-%m-%d %H:%M:%S')
        elif re.search("天前", dateStr):
            dayNum = int(re.sub('天前', '', dateStr))
            days = timedelta(days=dayNum)
            datetime2 = now - days
            return datetime2.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return now.strftime('%Y-') + dateStr + now.strftime(' %H:%M:%S')
