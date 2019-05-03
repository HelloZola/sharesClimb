# coding=utf-8
import os, sys
import time
import requests
import datetime
from lxml import etree

# 填充三位股票尾号
from com.vi.dao import SharesDao

pullcount = 0


def fillThreeNum(num):
    if num > 99:
        return str(num)
    elif num > 9:
        return "0" + str(num)
    else:
        return "00" + str(num)


# 保存拉取的股票结果(某年某个季度的股票数据)
def saveRecord(response, sharesCode):
    fields = ['shares_code', 'shares_name', 'data_date', 'start_price', 'top_price', 'low_price', 'end_price',
              'range_amount',
              'range_percent', 'volume_number', 'volume_amount', 'amplitude_percent', 'switch_percent', 'create_time',
              'update_time']
    html = etree.HTML(response.text, etree.HTMLParser())
    stockInfo = html.xpath('//div[@class="stock_info"]')
    # 判断是否存在股票
    if len(stockInfo) == 0:
        print("股票不存在：", sharesCode)
        return 0

    sharesPriceInfos = html.xpath('//table[contains(@class,"table_bg001")]/tr')

    # 判断该季度是否存在数据
    if len(sharesPriceInfos) == 0:
        return 1

    index = 1
    isConrinue = True
    rows = []
    localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    sharesNameStr = html.xpath('//span[@class="name"]//text()')
    sharesNameStrArr = sharesNameStr[0].split("(")
    sharesName = sharesNameStrArr[0]
    while isConrinue:
        sharesPriceInfo = html.xpath('//table[contains(@class,"table_bg001")]/tr[' + str(index) + ']//text()')
        index = index + 1
        if len(sharesPriceInfo) == 0:
            break
        else:
            row = []
            # 编码
            row.append(sharesCode)
            row.append(sharesName)
            # 日期
            if sharesPriceInfo[0].count("--") > 0:
                row.append(None)
            else:
                row.append(sharesPriceInfo[0])
            # 开盘价
            if sharesPriceInfo[1].count("--") > 0:
                row.append(None)
            else:
                row.append(sharesPriceInfo[1])
            # row.append(sharesPriceInfo[1].replace("--", ''))
            # 最高价
            if sharesPriceInfo[2].count("--") > 0:
                row.append(None)
            else:
                row.append(sharesPriceInfo[2])
            # row.append(sharesPriceInfo[2].replace("--", ''))
            # 最低价
            if sharesPriceInfo[3].count("--") > 0:
                row.append(None)
            else:
                row.append(sharesPriceInfo[3])
            # row.append(sharesPriceInfo[3].replace("--", ''))
            # 收盘价
            if sharesPriceInfo[4].count("--") > 0:
                row.append(None)
            else:
                row.append(sharesPriceInfo[4])
            # row.append(sharesPriceInfo[4].replace("--", ''))
            # 涨跌额
            if sharesPriceInfo[5].count("--") > 0:
                row.append(None)
            else:
                row.append(sharesPriceInfo[5])
            # row.append(sharesPriceInfo[5].replace("--", ''))
            # 涨跌幅
            if sharesPriceInfo[6].count("--") > 0:
                row.append(None)
            else:
                row.append(sharesPriceInfo[6])
            # row.append(sharesPriceInfo[6].replace("--", ''))
            # 成交量（手）
            if sharesPriceInfo[7].count("--") > 0:
                row.append(None)
            else:
                row.append(sharesPriceInfo[7].replace(",", ""))
            # row.append(sharesPriceInfo[7].replace("--", '').replace(",", ""))
            # 成交额（万元）
            if sharesPriceInfo[8].count("--") > 0:
                row.append(None)
            else:
                row.append(sharesPriceInfo[8].replace(",", ""))
            # row.append(sharesPriceInfo[8].replace("--", '').replace(",", ""))
            # 振幅( %)
            if sharesPriceInfo[9].count("--") > 0:
                row.append(None)
            else:
                row.append(sharesPriceInfo[9].replace("--", ''))
            # row.append(sharesPriceInfo[9].replace("--", ''))
            # 换手率( %)
            if sharesPriceInfo[10].count("--") > 0:
                row.append(None)
            else:
                row.append(sharesPriceInfo[10].replace("--", ''))
            # row.append(sharesPriceInfo[10].replace("--", ''))
            # 创建时间
            row.append(localTime)
            # 更新时间
            row.append(localTime)
            rows.append(row)
    if len(rows) > 0:
        SharesDao.insertMany(fields, rows, sharesCode)
    return 2


def noneAlter(str):
    if str == '':
        return None


# 根据股票编码进行拉取
def pullSharesInfo(sharesCode):
    curYear = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    curSeason = 4
    if month >= 10:
        curSeason = 4
    elif month >= 7:
        curSeason = 3
    elif month >= 4:
        curSeason = 2
    else:
        curSeason = 1
    isPull = True
    URL_GET = "http://quotes.money.163.com/trade/lsjysj_" + sharesCode + ".html"
    year = curYear
    maybeExist = 0
    while isPull:
        season = 4
        if year == curYear and season > curSeason:
            season = curSeason
        while season >= 1:
            param = {'year': year, 'season': season}
            response = requestpage(URL_GET, param, sharesCode, year, season)
            season = season - 1
            result = saveRecord(response, sharesCode)
            if result == 0:
                print("结束拉取", sharesCode)
                isPull = False
                break
            elif result == 1:

                # 如果最近的这个季度都没有，那么就没必要继续拉取了
                if maybeExist == 0:
                    if year == curYear and season == curSeason:
                        isPull = False
                        break
                # 否则再拉取几个季度看看，如果连续超过5个季度都没有，那么就结束拉取当前这支股票
                # （这样做的原因是有些股票（如万科A - 2016年6月左右）中间有一段时间是没有数据的）
                maybeExist = maybeExist + 1
                print("季度数据不存在:", sharesCode, maybeExist)
                if maybeExist > 5:
                    isPull = False
                    break
            elif result == 2:
                maybeExist = 0
                continue
            else:
                print("发现特殊result:", result, "进入睡眠")
                time.sleep(180)
                print("唤醒睡眠")
        year = year - 1


# 拉取报错时进行休息，休息完成后继续拉取
def requestpage(URL_GET, param, sharesCode, year, season):
    while True:
        try:
            response = requests.get(URL_GET, params=param)
            return response
        except Exception as err:
            print(err)
            time.sleep(10)
        finally:
            print("已拉取!", sharesCode, year, season)


# 1.获取股票代码  - 休息重试模式
def startX():
    # 已经拉取过的股票编码开头,方便手动控制，不必每次都从头开始拉取
    alreadyStartHead = "000049"

    starttime = datetime.datetime.now()  ##开始时间
    sharesHeads = ['000', '002', '300', '600', '601', '603']

    for sharesHead in sharesHeads:

        count = 0
        while count <= 999:

            sharesCode = sharesHead + fillThreeNum(count)

            if alreadyStartHead is not None:
                if alreadyStartHead > sharesCode:
                    print("股票已经拉起，跳过：", sharesCode)
                    count = 1 + count
                    continue
            pullSharesInfo(sharesCode)
            print("股票编码：" + sharesCode)
            count = 1 + count

    endtime = datetime.datetime.now()  ##开始时间
    print("用时（s）：", (endtime - starttime).seconds)


##开始拉取
startX()

