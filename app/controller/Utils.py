import datetime
import hashlib
import os

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