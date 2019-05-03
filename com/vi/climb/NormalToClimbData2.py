# coding=utf-8
import os, sys
import time

import requests
import datetime
from lxml import etree, html


def fillThreeNum(num):
    if num > 99:
        return str(num)
    elif num > 9:
        return "0" + str(num)
    else:
        return "00" + str(num)


def saveRecord(response):
    html = etree.HTML(response.text, etree.HTMLParser())
    stockInfo = html.xpath('//div[@class="stock_info"]')
    if stockInfo is None:
        return False
    sharesPriceInfos = html.xpath('//table[contains(@class,"table_bg001")]/tr')

    if sharesPriceInfos is null:
        return False


def pullSharesInfo(sharesCode):
    year = int(str(time.tm_year))
    isPull = True
    URL_GET = "http://quotes.money.163.com/trade/lsjysj_600508.html"
    while isPull:
        season = 4
        while season >= 1:
            param = {'year': year, 'season': season}
            response = requests.get(URL_GET, params=param)
            season = season - 1

        year = year - 1


# 1.获取股票代码  - 休息重试模式
def startX():
    # starttime = datetime.datetime.now()  ##开始时间
    # sharesHeads = ['000', '002', '300', '600', '601', '603']
    #
    # for sharesHead in sharesHeads:
    #     count = 0
    #     while count <= 999:
    #         sharesCode = sharesHead + fillThreeNum(count)
    #         print("股票编码：" + sharesCode)
    #         count = 1 + count
    #
    # endtime = datetime.datetime.now()  ##开始时间
    # print("用时（s）：", (endtime - starttime).seconds)

    print(datetime.datetime.now().year)
    URL_GET = "http://quotes.money.163.com/trade/lsjysj_500508.html"
    # # baseUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/"
    # # provinceFile = open("G:\\Tem\\area_citys.csv", "w")
    param = {'year': '2015', 'season': '2'}
    response = requests.get(URL_GET, params=param)
    html = etree.HTML(response.text, etree.HTMLParser())
    # # sharesname = html.xpath('//span[@class="name"]/text()')
    sharesPriceInfos = html.xpath('//table[contains(@class,"table_bg001")]/tr')
    if len(sharesPriceInfos)==0:
        print("none")
    else:
        print("not none")

    stockInfo = html.xpath('//div[@class="stock_info"]')
    if len(stockInfo) == 0:
        print("none")
    else:
        print("not none")

    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    curSeason = 1
    if month >= 10:
        curSeason = 4
    elif month >= 7:
        curSeason = 3
    elif month >= 4:
        curSeason = 2
    else:
        curSeason = 1
    print(curSeason)

    # # print(sharesname)
    # print(sharesPriceInfo)
    # print(sharesPriceInfo[1])
    # print(sharesPriceInfo[2])
    # print(sharesPriceInfo[3])
    # print(etree.tostring(html,method='html',encoding='unicode'))
    # doc = html.fromstring(response.text)
    # print(html.tostring(doc,method='html',encoding='unicode'))
    # print(response.headers)
    # print(response.status_code)
    # print(response.text)


##开始拉取
startX()

# countyInfo = {'name': "长安区", 'address': "01/130102.html", 'code': "130102000000", 'lastCode':"130000000000"}
# baseUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/13/"
# Towntrs = getTowntrs(countyInfo, baseUrl)
# for towntr in Towntrs:
#     print towntr.get("lastCode")," ",towntr.get("code")," ",towntr.get("name")," ",towntr.get("address")


# tower = {'name': "长安区", 'address': "01/130102.html", 'code': "130102000000", 'lastCode':"130000000000"}
# baseUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/13/"
# Towntrs = getTowntrs(tower, baseUrl)
# for towntr in Towntrs:
#     print towntr.get("lastCode")," ",towntr.get("code")," ",towntr.get("name")," ",towntr.get("address")


# tower = {'name': "常张乡", 'address': "28/140428202.html", 'code': "440103001000", 'lastCode':"130000000000"}
# baseUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/14/04/"
# Villagetrs = getVillagetrs(tower, baseUrl)
# for Villagetr in Villagetrs:
#     print Villagetr.get("lastCode")," ",Villagetr.get("code")," ",Villagetr.get("name")," ",Villagetr.get("address")," ",Villagetr.get("town&countryType")
