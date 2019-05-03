import pymysql
import os
import configparser


def getDB():
    # 打开数据库连接
    # 获取文件的当前路径（绝对路径）
    # cur_path = os.path.dirname(os.path.realpath(__file__))
    cur_path = "E:\workspaceForPython\sharesClimb\config\mysql.conf"
    # config_path = os.path.join(cur_path, 'config/config.ini')
    conf = configparser.ConfigParser()
    conf.read(cur_path)
    url = conf.get('Mysql', 'url')
    server = conf.get('Mysql', 'server')
    username = conf.get('Mysql', 'username')
    password = conf.get('Mysql', 'password')
    db = pymysql.connect(url, username, password, server)
    return db


def excuteInsertManyDIY(sql, fields, rows):
    # 获取cursor
    db = getDB()
    cursor = db.cursor()
    try:
        cursor.executemany(sql, rows)
        # 事务提交
        db.commit()
    except Exception as err:
        print(err)
    finally:
        # 关闭数据库连接
        db.close()


def excuteInsertMany(tableName, fields, rows, isIgnore):
    ignore = ""
    if isIgnore:
        ignore = "IGNORE"
    sql = "INSERT " + ignore + " INTO " + tableName + "({fields}) VALUE ({mark});".format(
        fields='`' + '`,`'.join(fields) + '`', mark=','.join(['%s'] * len(fields)))

    # 获取cursor
    db = getDB()
    cursor = db.cursor()
    try:
        cursor.executemany(sql, rows)
        # 事务提交
        db.commit()
    # except Exception as err:
    #     print(err)
    finally:
        # 关闭数据库连接
        db.close()


def excuteInsert(tableName, fields, rows, isIgnore):
    ignore = ""
    if isIgnore:
        ignore = "IGNORE"
    sql = "INSERT " + ignore + " INTO " + tableName + "({fields}) VALUE ({mark});".format(
        fields='`' + '`,`'.join(fields) + '`', mark=','.join(['%s'] * len(fields)))

    # 获取cursor
    db = getDB()
    cursor = db.cursor()
    try:
        cursor.execute(sql, rows)
        # 事务提交
        db.commit()
    finally:
        # 关闭数据库连接
        db.close()


def select(sql):
    # 获取cursor
    db = getDB()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        alldata = cursor.fetchall()
        return alldata
    except Exception as err:
        print(err)
    finally:
        # 关闭数据库连接
        db.close()

# cur_path = os.path.dirname(os.path.realpath(__file__))
# config_path = os.path.join(cur_path, 'config.ini')

# config_path = "E:\workspaceForPython\sharesClimb\config.conf"
# conf = configparser.ConfigParser()
# conf.read(config_path)
# # mail_server = conf.get('Mysql', 'url')
# print(conf.sections())
# print(mail_server)
# 打开数据库连接
# 获取文件的当前路径（绝对路径）
# # cur_path = os.path.dirname(os.path.realpath(__file__))
# file_path = 'filename.properties'
# props = property.parse(file_path)
# print(props.get('server'))

# conf = configparser.ConfigParser()
# conf = configparser.ConfigParser()
# conf.read("config.conf")
# url = conf.get('Mysql', 'url')
# server = conf.get('Mysql', 'server')
# username = conf.get('Mysql', 'username')
# password = conf.get('Mysql', 'password')
# print(url)
# print(server)
# print(username)
# print(password)


# db = pymysql.connect("localhost", "root", "chenkangliu", "shares")
# # 使用 cursor() 方法创建一个游标对象 cursor
# cursor = db.cursor()
# fields = ['code', 'data_date', 'start_price', 'top_price', 'low_price', 'end_price', 'range_amount', 'range_percent', 'volume_number', 'volume_amount', 'amplitude_percent', 'switch_percent', 'create_time', 'update_time']
# sql = "INSERT IGNORE INTO shares_trades ({fields}) VALUE ({mark});".format(fields='`' + '`,`'.join(fields) + '`',
#                                                                     mark=','.join(['%s'] * len(fields)))
# sql = """
#     INSERT INTO tt ({fields}) VALUE ({mark});
#     """.format(
#     fields='`' + '`,`'.join(fields) + '`',
#     mark=','.join(['%s'] * len(fields))
# )
#
# rows = []
#
# row1 = ['000000', '2019-04-30', '10.37', '10.50', '10.32', '10.45', '0.10', '0.97', '26154', '2729', '1.74', '0.36', '2019-05-03 22:51:59', '2019-05-03 22:51:59']
# # row1.append("code1")
# # row1.append("123")
#
# row2 = ['000000', '2019-04-31', '10.37', '10.50', '10.32', '10.45', '0.10', '0.97', '26154', '2729', '1.74', '0.36', '2019-05-03 22:51:59', '2019-05-03 22:51:59']
# # row2.append("code2")
# # row2.append("124")
#
# rows.append(row1)
# rows.append(row2)
# cursor.executemany(sql, rows)
# db.commit()
# # print("Database version : %s " % data)
#
# # 关闭数据库连接
# db.close()
