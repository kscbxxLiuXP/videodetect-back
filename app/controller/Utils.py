import datetime
import hashlib
import os
import time
# 获取文件MD5值
import cv2
from flask import make_response, jsonify

from app.controller import Connection


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
    return myhash.hexdigest()


# 生成时间ID
def generate_timeID():
    return '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now())


# 时间格式化
def time_format():
    return '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())


# 获取文件大小
def get_file_size(path):
    size = os.path.getsize(path)
    return size


# 根据byte大小，生成对应的文件大小 KB,MB,GB
def size_format(size):
    if size < 1000:
        return '%i' % size + 'size'
    elif 1000 <= size < 1000000:
        return '%.1f' % float(size / 1000) + 'KB'
    elif 1000000 <= size < 1000000000:
        return '%.1f' % float(size / 1000000) + 'MB'
    elif 1000000000 <= size < 1000000000000:
        return '%.1f' % float(size / 1000000000) + 'GB'
    elif 1000000000000 <= size:
        return '%.1f' % float(size / 1000000000000) + 'TB'


def getVideoInfo(input_video):
    capture = cv2.VideoCapture(input_video)
    totalFrameNumber = capture.get(7);
    FPS = capture.get(5)  # 这个是获取视频帧率
    info = {}
    info['fps'] = FPS
    info['length'] = frames_to_timecode(FPS, totalFrameNumber)
    return info


def frames_to_timecode(framerate, frames):
    """
    视频 通过视频帧转换成时间
    :param framerate: 视频帧率
    :param frames: 当前视频帧数
    :return:时间（00:00:01:01）
    """
    return '{0:02d}:{1:02d}:{2:02d}:{3:02d}'.format(int(frames / (3600 * framerate)),
                                                    int(frames / (60 * framerate) % 60),
                                                    int(frames / framerate % 60),
                                                    int(frames % framerate))


# code:结果代码 0执行成功 1执行失败
# message:返回信息
# data:如需返回data data是对象{}
def responseGen(code, message, data):
    body = {
        'code': code,
        'msg': message,
        'data': data
    }
    res = make_response(jsonify(body))
    # 添加跨域headers 实现对前端Axios Ajax的支持
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Method'] = '*'
    res.headers['Access-Control-Allow-Headers'] = '*'
    return res


def sendNotice_startDetect(id):
    new_db = Connection.newConnection()
    new_cursor = new_db.cursor()
    sql = "select * from video where videoid = '%s'" % (id)
    new_cursor.execute(sql)
    record = new_cursor.fetchone()
    receiver = record[8]
    videoname = record[1]
    content = """<p>尊敬的 <strong><ins>%s</ins></strong> 您好：</p>
<br></br>
<br></br>
<p style="text-align:center;">您上传的视频 <span style="color: rgb(84,172,210);"><code><strong>%s</strong></code></span> 正在检测中</p>
<p style="text-align:center;">详情前往 <a href="http://127.0.0.1:3000/#/home/content/%s" target="_blank">此处</a> 查看</p>
<br></br>
<p style="text-align:right;"><strong><em>VideoDetect</em></strong></p>
<p style="text-align:right;">保护您的创作权益</p>
<p style="text-align:right;">%s&nbsp;</p>
""" % (receiver, videoname, id, time_format())
    sql = "INSERT INTO message (`mFrom`,`mTo`,`content`,`sendTime`,`readed`,`subject`) VALUES ('SYSTEM','%s','%s','%s',0,'通知-检测开始-%s');" % (
        receiver, content, time_format(), videoname)
    new_cursor.execute(sql)
    new_db.commit()
    new_db.close()


def sendNotice_finishDetect(id):
    new_db = Connection.newConnection()
    new_cursor = new_db.cursor()
    sql = "select * from video where videoid = %s" % (id)
    new_cursor.execute(sql)
    record = new_cursor.fetchone()
    receiver = record[8]
    videoname = record[1]
    content = """<p>尊敬的 <strong><ins>%s</ins></strong> 您好：</p>
<br></br>
<br></br>
<p style="text-align:center;">您上传的视频 <span style="color: rgb(84,172,210);"><code><strong>%s</strong></code></span> 检测已完成</p>
<p style="text-align:center;">详情前往 <a href="http://127.0.0.1:3000/#/home/content/%s" target="_blank">此处</a> 查看</p>
<br></br>
<p style="text-align:right;"><strong><em>VideoDetect</em></strong></p>
<p style="text-align:right;">保护您的创作权益</p>
<p style="text-align:right;">%s&nbsp;</p>
""" % (receiver, videoname, id, time_format())
    sql = "INSERT INTO message (`mFrom`,`mTo`,`content`,`sendTime`,`readed`,`subject`) VALUES ('SYSTEM','%s','%s','%s',0,'通知-检测结束-%s');" % (
        receiver, content, time_format(), videoname)
    new_cursor.execute(sql)
    new_db.commit()
    new_db.close()


def sendMessage_fedbkReply(id):
    new_db = Connection.newConnection()
    new_cursor = new_db.cursor()
    sql = "select * from feedback where id = '%s'" % (id)
    new_cursor.execute(sql)
    re = new_cursor.fetchone()
    time = time_format()
    title = re[1]
    content = re[2]
    smtPerson = re[3]
    applier = re[5]
    applyContent = re[6]
    smtTime = str(re[7])
    applyTime = str(re[8])

    content = """<p>尊敬的
        <u>%s</u>您好：</p>
    <p>
        <br>
    </p>
    <p class="ql-indent-1">感谢您给我们的反馈，我们对您的反馈做出了如下回复：</p>
    <p class="ql-indent-1">
        <br>
    </p>
    <p class="ql-indent-1">反馈人：%s</p>
    <p class="ql-indent-1">反馈时间：%s</p>
    <p class="ql-indent-1">问题概要：%s</p>
    <p class="ql-indent-1">反馈内容：%s</p>
    <p class="ql-indent-1">---------------------------</p>
    <p class="ql-indent-1">处理人：%s</p>
    <p class="ql-indent-1">处理时间：%s</p>
    <p class="ql-indent-1">回复：%s</p>
    <p class="ql-indent-1">
        <br>
    </p>
    <p class="ql-indent-1">
        <br>
    </p>
    <p class="ql-indent-1 ql-align-right">
        <strong>
            <em>
                <u>VideoDetect</u>
            </em>
        </strong>
    </p>
    <p class="ql-indent-1 ql-align-right">保护您的视频版权</p>
    <p class="ql-indent-1 ql-align-right">%s</p>""" % (
        smtPerson, smtPerson, smtTime, title, content, applier, applyTime, applyContent, time)
    sql = "INSERT INTO message (`mFrom`,`mTo`,`content`,`sendTime`,`readed`,`subject`) VALUES ('SYSTEM','%s','%s','%s',0,'回复-反馈-%s');" % (
        smtPerson, content, time_format(), title)
    new_cursor.execute(sql)
    new_db.commit()
    new_db.close()


def getLastYearTodayTime():
    # date = '2020-10-12 14:02'
    # timeArray = time.strptime(date, "%Y-%m-%d %H:%M")
    # timeStamp = (time.mktime(timeArray))  # 转化为时间戳
    timeStamp = time.time()
    end_time = time.strftime('%Y-%m-%d', time.localtime(timeStamp))
    start_year = int(time.strftime('%Y', time.localtime(timeStamp))) - 1
    month_day = time.strftime('%m-%d', time.localtime(timeStamp))
    start_time = '{}-{} 00:00:00'.format(start_year, month_day)
    return start_time


def getYearDateSequence():
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
    return data_year_month


def getMonthDate():
    begin_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    b_date = begin_date + " 00:00:00"
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return b_date,date_list

def getWeekDate():
    begin_date = (datetime.datetime.now() - datetime.timedelta(days=6)).strftime("%Y-%m-%d")
    b_date = begin_date + " 00:00:00"
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return b_date,date_list

def DateListMatchSql(dateSequence, sqlData):
    data = []
    for date in dateSequence:
        if sqlData.__contains__(date):
            data.append(sqlData[date])
        else:
            data.append(0)
    return data
