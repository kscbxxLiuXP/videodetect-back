import datetime
import hashlib
import json
import os
import numpy as np
from os import listdir
import calendar
from flask import safe_join

import app.controller.MySqlUtil as DBUtil
import app.controller.FileUtil as FileUtil
import app.controller.Utils as Utils
import config
from app.controller import Connection
from app.controller.algorithms.ImageNNExtract import imageNNExtract
import threading
import time


def get_file_md5(filepath):
    # 获取文件的md5
    if not os.path.isfile(filepath):
        return
    myhash = hashlib.md5()
    f = open(filepath, "rb")
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    print(myhash.hexdigest())
    return myhash.hexdigest()


def tid_maker():
    return '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now())


def time_format():
    return '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())


class MyThread(threading.Thread):
    def __init__(self, n):
        super(MyThread, self).__init__()  # 重构run函数必须要写
        self.n = n

    def run(self):
        print("task", self.n)
        time.sleep(1)
        print('2s')
        time.sleep(1)
        print('1s')
        time.sleep(1)
        print('0s')
        time.sleep(1)


def save_dic():
    dic = {
        'andy': {
            'age': 23,
            'city': 'beijing',
            'skill': 'python'
        },
        'william': {
            'age': 25,
            'city': 'shanghai',
            'skill': 'js'
        }
    }
    print(dic)
    js = json.dumps(dic)
    file = open('test.txt', 'w')
    file.write(js)
    file.close()


def read_json():
    file = open('test.txt', 'r')
    js = file.read()
    dic = json.loads(js)
    print(dic["andy"])
    file.close()


def sendNotice_startDetect(id):
    new_db = Connection.newConnection()
    new_cursor = new_db.cursor()
    sql = "select * from video where videoid = '%s'" % (id)
    new_cursor.execute(sql)
    record = new_cursor.fetchone()
    receiver = record[8]
    videoname = record[1]
    print(receiver)
    print(videoname)
    content = """<p>尊敬的 <strong><ins>%s</ins></strong> 您好：</p>
<br></br>
<br></br>
<p style="text-align:center;">您上传的视频 <span style="color: rgb(84,172,210);"><code><strong>%s</strong></code></span> 正在检测中</p>
<p style="text-align:center;">详情前往 <a href="http://127.0.0.1/#/home/content/%s" target="_blank">此处</a> 查看</p>
<br></br>
<p style="text-align:right;"><strong><em>VideoDetect</em></strong></p>
<p style="text-align:right;">保护您的创作权益</p>
<p style="text-align:right;">%s&nbsp;</p>
""" % (receiver, videoname, id, time_format())
    print(content)
    sql = "INSERT INTO message (`mFrom`,`mTo`,`content`,`sendTime`,`readed`,`subject`) VALUES ('SYSTEM','%s','%s','%s',0,'通知-检测开始');" % (
        receiver, content, time_format())
    new_cursor.execute(sql)
    new_db.commit()
    new_db.close()


def testDate():
    # 获取年、月
    this_year = datetime.now().year
    this_month = datetime.now().month

    date_list = [[this_year, this_month, calendar.monthlen(this_year, this_month)]]
    for i in range(5):
        year_month_days = list(calendar.prevmonth(this_year, this_month))
        this_month = this_month - 1
        if this_month <= 0:
            this_month = 12
            this_year = this_year - 1
        year_month_days.append(calendar.monthlen(this_year, this_month))
        date_list.append(year_month_days)

    for date_tuple in date_list:
        if date_tuple[1] < 10:
            date_tuple[1] = "0" + str(date_tuple[1])

    print(date_list)


def getYearTime():
    date = '202010121402'
    a = time.time()
    print(a)
    timeArray = time.strptime(date, "%Y%m%d%H%M")
    timeStamp = (time.mktime(timeArray))  # 转化为时间戳
    print(timeStamp)
    end_time = time.strftime('%Y-%m-%d', time.localtime(timeStamp))
    start_year = int(time.strftime('%Y', time.localtime(timeStamp))) - 1
    month_day = time.strftime('%m-%d', time.localtime(timeStamp))
    start_time = '{}-{} 00:00:00'.format(start_year, month_day)
    print(start_time)


def getMonthDate():

    begin_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    b_date=begin_date +" 00:00:00"
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    print(b_date)
    print(date_list)


def getWeekDate():
    date = '20201011'
    dt = datetime.datetime.strptime(date, "%Y%m%d")
    oneweek = datetime.timedelta(weeks=1)
    yesterweek = dt - oneweek
    print(yesterweek)


def getYearMonth():
    # 得到现在的时间  得到now等于2016年9月25日
    now = datetime.datetime.now()
    # 得到今年的的时间 （年份） 得到的today_year等于2016年
    today_year = now.year
    # 今年的时间减去1，得到去年的时间。last_year等于2015
    last_year = int(now.year) - 1
    # 得到今年的每个月的时间。today_year_months等于1 2 3 4 5 6 7 8 9，
    today_year_months = range(1, now.month + 1)
    # 得到去年的每个月的时间  last_year_months 等于10 11 12
    last_year_months = range(now.month + 1, 13)
    # 定义列表去年的数据
    data_list_lasts = []
    # 通过for循环，得到去年的时间夹月份的列表
    # 先遍历去年每个月的列表
    for last_year_month in last_year_months:
        # 定义date_list 去年加上去年的每个月
        date_list = '%s-%02d' % (last_year, last_year_month)
        # 通过函数append，得到去年的列表
        data_list_lasts.append(date_list)

    data_list_todays = []
    # 通过for循环，得到今年的时间夹月份的列表
    # 先遍历今年每个月的列表
    for today_year_month in today_year_months:
        # 定义date_list 去年加上今年的每个月
        data_list = '%s-%02d' % (today_year, today_year_month)
        # 通过函数append，得到今年的列表
        data_list_todays.append(data_list)
    # 去年的时间数据加上今年的时间数据得到年月时间列表
    data_year_month = data_list_lasts + data_list_todays

    print(data_year_month)


def getRecentYearData():
    new_db = Connection.newConnection()
    new_cursor = new_db.cursor()
    lastYearToday = Utils.getLastYearTodayTime()
    sql = """SELECT 
              DATE_FORMAT(`VideoUploadTime`, '%Y-%m') months,
              count(*) sum
              FROM
              video
              WHERE `VideoUploadTime` > '{}'
              GROUP BY months ;
              """.format(lastYearToday)
    new_cursor.execute(sql)
    records = new_cursor.fetchall()
    dateSequence = Utils.getYearDateSequence()
    data = {}
    for re in records:
        data[re[0]] = re[1]
    print(Utils.DateListMatchSql(dateSequence, data))


if __name__ == "__main__":
    # from app.controller.algorithms.VideoDetect import videoDetect
    # path = 'C:/Users/LIUXP/Pictures/111.png'
    # md5 = '534ebc37e160d58f1561dc4ad86c9b95'
    id = '417605300'
    # DBUtil.getVideoInfo(id)
    # video = DBUtil.getVideo(id)
    # path = FileUtil.getVideoDir(id)
    # name = id + '.' + video.get('type')
    # filename = os.fspath(name)
    # directory = os.fspath(path)
    # filename = safe_join(directory, filename)
    # videoDetect(id)
    # imageNNExtract("D:/大创/项目代码/website/data/DetectTmp/20200516190554330544")

    # info=DBUtil.getVideoInfo('20200608222651575457')
    # print(info)
    # sendNotice_startDetect(id)
    # getYearTime()
    # getYearMonth()
    # getMonthDate()
    # getWeekDate()
    # print(Utils.getMonthDate())
    # print(Utils.getWeekDate())
    # getRecentYearData()
    list=['s']
    print(list.__len__())