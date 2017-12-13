# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhufanginfoItem(scrapy.Item):
    '''租赁房屋信息'''
    # define the fields for your item here like:
    title = scrapy.Field()  # 标题
    roomLink = scrapy.Field()  # 链接
    price = scrapy.Field()  # 价格
    payType = scrapy.Field()  # 支付方式
    rentType = scrapy.Field()  # 租赁方式
    bedRoomType = scrapy.Field()  # 卧室类型
    sexLimit = scrapy.Field()  # 性别限制
    roomType = scrapy.Field()  # 房屋类型
    roomSize = scrapy.Field()  # 房屋大小
    decorationType = scrapy.Field()  # 装修方式
    orientation = scrapy.Field()  # 朝向
    floor = scrapy.Field()  # 楼层
    houseArea = scrapy.Field()  # 住宅小区
    longitude = scrapy.Field()  # 经度
    latitude = scrapy.Field()  # 纬度
    thirdDistrict = scrapy.Field()  # 三级行政区域
    secondDistrict = scrapy.Field()  # 二级行政区域
    firstDistrict = scrapy.Field()  # 一级行政区域
    subwayDistance = scrapy.Field()  # 最近地铁站距离
    address = scrapy.Field()  # 详细地址
    cellphone = scrapy.Field()  # 联系电话
    bed = scrapy.Field()  # 床
    chest = scrapy.Field()  # 衣柜
    sofa = scrapy.Field()  # 沙发
    telev = scrapy.Field()  # 电视
    icebox = scrapy.Field()  # 冰箱
    washer = scrapy.Field()  # 洗衣机
    airCondition = scrapy.Field()  # 空调
    waterHeater = scrapy.Field()  # 热水器
    centralHeater = scrapy.Field()  # 暖气
    balcony = scrapy.Field()  # 阳台
    toilet = scrapy.Field()  # 独立卫生间
    roomPictureLink = scrapy.Field()  # 房屋照片地址，多个用分号隔开
    publishPerson = scrapy.Field()  # 信息发布者
    publishOrg = scrapy.Field()  # 信息发布者公司
    publishType = scrapy.Field()  # 信息发布类型（个人，经纪人，品牌公寓）
    publishTime = scrapy.Field()  # 信息发布时间
