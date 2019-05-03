from datetime import time

from com.vi.dao import db

tableName = "shares_trades"


# 批量插入数据
def insertMany(fields, rows, sharesCode):
    try:
        db.excuteInsertMany(tableName, fields, rows, True)
    except Exception as err:
        print("股票拉取数据发生异常:", sharesCode)
        print(err)
        print("进入睡眠")
        time.sleep(180)
        print("唤醒睡眠")
        fields_qus = ['shares_code', 'err']
        rows_qus = []
        rows_qus.append(sharesCode)
        rows_qus.append(err)
        db.excuteInsert("question_shares", fields_qus, rows_qus, True)


def selectSumLowerShares():
    dataList = db.select("select sumcount,shares_code from ("
                         "SELECT SUM(1)as sumcount,shares_code FROM shares_trades GROUP BY shares_code) tem "
                         "where sumcount<4000 order by shares_code desc")
    return dataList