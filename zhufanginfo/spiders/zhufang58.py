import scrapy, re, math
from datetime import datetime
from datetime import timedelta


class Zhufang58Spider(scrapy.Spider):
    name = 'zhufang58'
    # 减慢爬取速度 为1s
    download_delay = 1
    allowed_domains = ['58.com']
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

        nextPage = sel.xpath('//li[@id="bottom_ad_li"]/div[@class="pager"]/a[@class="next"]/@href').extract_first()
        if nextPage is not None:
            yield response.follow(nextPage.strip(), self.parse)

    def parse_room(self, response):
        def response_to_xpath(query):
            if response.xpath(query).extract_first() == None:
                return ''
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
        rentTypeInfo = response_to_xpath('//ul[@class="f14"]/li[1]/span[2]/text()')
        rentTypeInfoSearchObj = re.search('(.*)-(.*)-(.*)', rentTypeInfo)
        if rentTypeInfoSearchObj:
            rentType = rentTypeInfoSearchObj.group(1).strip()  # 租赁方式
            bedRoomType = rentTypeInfoSearchObj.group(2).strip()  # 卧室类型
            sexLimit = rentTypeInfoSearchObj.group(3).strip()  # 性别限制
        else:
            rentType = rentTypeInfo
            bedRoomType = ''
            sexLimit = ''

        # 房屋信息
        houseInfo = response_to_xpath('//ul[@class="f14"]/li[2]/span[2]/text()')
        houseInfoSearchObj = re.search('(\S*)(.*)平(.*)', houseInfo)
        if houseInfoSearchObj:
            roomType = houseInfoSearchObj.group(1).strip()  # 房屋类型
            roomSize = houseInfoSearchObj.group(2).strip()  # 房屋大小
            decorationType = houseInfoSearchObj.group(3).strip()  # 装修方式
        else:
            roomType = ''
            roomSize = ''
            decorationType = ''

        # 朝向楼层信息
        floorInfo = response_to_xpath('//ul[@class="f14"]/li[3]/span[2]/text()')
        floorInfoSearchObj = re.search('(\S*)(.*)', floorInfo)
        if floorInfoSearchObj:
            orientation = floorInfoSearchObj.group(1).strip()  # 朝向
            floor = floorInfoSearchObj.group(2).strip()  # 楼层
        else:
            orientation = ''
            floor = ''

        # 住宅小区
        houseArea = response_to_xpath('//ul[@class="f14"]/li[4]/span[2]/a/text()')
        # 二级行政区域
        secondDistrict = response_to_xpath('//ul[@class="f14"]/li[5]/span[2]/a[1]/text()')
        # 三级行政区域
        thirdDistrict = response_to_xpath('//ul[@class="f14"]/li[5]/span[2]/a[2]/text()')
        # 最近地铁站距离
        subwayDistance = response_to_xpath('//ul[@class="f14"]/li[5]/em/text()')
        # 详细地址
        address = response_to_xpath('//ul[@class="f14"]/li[6]/span[2]/text()')
        # 联系电话
        cellphone = response_to_xpath('//span[@class="house-chat-txt"]/text()')
        # 信息发布者信息
        publishPersonInfo = response_to_xpath('//p[@class="agent-name f16 pr"]/a/text()')
        publishPersonInfoSearchObj = re.search('(\S*)\((.*)\)', publishPersonInfo)
        if publishPersonInfoSearchObj:
            publishPerson = publishPersonInfoSearchObj.group(1).strip()  # 发布人
            publishType = publishPersonInfoSearchObj.group(2).strip()  # 信息发布类型
        else:
            publishPerson = ''
            publishType = ''

        # 经纬度
        location = response_to_xpath('//div[@class="view-more-detailmap view-more"]/a/@href')
        locationSearchObj = re.search('(.*)location=(.*),(.*)&title=(.*)', location)
        if locationSearchObj:
            latitude = locationSearchObj.group(2).strip()  # 纬度
            longitude = locationSearchObj.group(3).strip()  # 经度
        else:
            latitude = ''
            longitude = ''

        print("标题：" + title)
        print("发布时间：" + publishTime)
        print("租金：" + price)
        print("支付方式：" + payType)
        print("租赁方式：" + rentType)
        print("卧室类型：" + bedRoomType)
        print("性别限制：" + sexLimit)
        print("房屋类型：" + roomType)
        print("房屋大小：" + roomSize)
        print("装修方式：" + decorationType)
        print("朝向：" + orientation)
        print("楼层：" + floor)
        print("住宅小区：" + houseArea)
        print("二级行政区域：" + secondDistrict, )
        print("三级行政区域：" + thirdDistrict)
        print("最近地铁站距离：" + subwayDistance)
        print("详细地址：" + address)
        print("联系电话：" + cellphone)
        print("发布人：" + publishPerson)
        print("发布类型：" + publishType)
        print("纬度：" + latitude)
        print("经度：" + longitude, end="\r\n\r\n")

    def formatTime(self, dateStr):
        now = datetime.now()

        reg = '房源编号：(\S*)\xa0\xa0\xa0\xa0\r\n(.*)'
        if re.search(reg, dateStr):
            searchObj = re.search(reg, dateStr)
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
