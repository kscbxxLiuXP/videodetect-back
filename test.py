import datetime
import hashlib
import json
import os
import numpy as np
from os import listdir

from flask import safe_join

import app.controller.MySqlUtil as DBUtil
import app.controller.FileUtil as FileUtil
import app.controller.Utils as Utils
import config
from app.controller import Connection
from app.controller.algorithms.ImageNNExtract import imageNNExtract


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


import threading
import time


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
    sql="select * from video where videoid = '%s'"%(id)
    new_cursor.execute(sql)
    record=new_cursor.fetchone()
    receiver=record[8]
    videoname=record[1]
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
    sendNotice_startDetect(id)