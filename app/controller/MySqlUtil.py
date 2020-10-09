# -*- coding:utf-8 -*-
import MySQLdb
import json

from flask import Response

from app.controller import Utils
import config
import datetime

db = MySQLdb.connect(
    "localhost",
    config.SQL_USERNAME,
    config.SQL_PSD,
    "videodetect",
    charset='utf8'
)

cursor = db.cursor()


def newConnection():
    new_db = MySQLdb.connect(
        "localhost",
        config.SQL_USERNAME,
        config.SQL_PSD,
        "videodetect",
        charset='utf8'
    )
    return new_db


def getUserList():
    tableName = 'user'
    sql = "select * from %s " % (tableName)
    cursor.execute(sql)

    listAll = cursor.fetchall()  # fetchall() 获取所有记录
    userlist = []
    i = 1
    for record in listAll:
        job = {
            'username': record[0],
            'avatar': record[11],
            'key': record[0],
            'password': record[1],
            'email': record[2],
            'age': record[3],
            'sex': record[4],
            'level': record[6],
            'nickname': record[7],
            'birth': datetime.datetime.strftime(record[8], '%Y-%m-%d'),
            'phone': record[9],
            'sign': record[10],
            'registerTime': str(record[12])
        }
        i = i + 1
        userlist.append(job)

    json_str = json.dumps(userlist)
    return json_str


def getFeatureList():
    tableName = 'feature'
    sql = "select * from %s " % (tableName)
    cursor.execute(sql)

    listAll = cursor.fetchall()  # fetchall() 获取所有记录
    userlist = []
    i = 1
    for item in listAll:
        job = {
            'key': i,
            'icon': "http://127.0.0.1:5000/api/pic/" + item[0],
            'featureid': item[0],
            'featuretime': item[2],
            'featurearg': str(item[3]),
        }
        i = i + 1
        userlist.append(job)

    json_str = json.dumps(userlist)
    return json_str


def checkUser(username):
    tableName = 'user'
    sql = " select count(*) from %s where username='%s'" % (tableName, username);
    cursor.execute(sql)

    listAll = cursor.fetchall()  # fetchall() 获取所有记录
    num = listAll[0][0]
    if num == 1:
        return 1
    else:
        return 0


def checkPassword(username, password):
    tableName = 'user'
    sql = " select userpassword,admined from %s where username='%s'" % (tableName, username);
    cursor.execute(sql)

    listAll = cursor.fetchall()  # fetchall() 获取所有记录
    psd = listAll[0][0]
    admined = listAll[0][1]
    re = {}
    if psd == password:
        re = {'code': 1, 'admined': admined}
    else:
        re = {'code': 0}
    return re


def checkFileMD5(md5):
    tableName = 'video'
    sql = " select count(*) from %s where VideoMd5='%s'" % (tableName, md5);
    cursor.execute(sql)

    listAll = cursor.fetchall()  # fetchall() 获取所有记录
    num = listAll[0][0]
    if num >= 1:
        return 1
    else:
        return 0


def registerUser(json_str):
    try:
        user = json.loads(json_str)
        username = user.get('username')
        password = user.get('password')
        nickname = user.get('nickname')
        sex = user.get('sex')
        age = user.get('age')
        birth = user.get('birth')
        email = user.get('email')
        phone = user.get('phone')
        registerTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        sql = "insert into user(UserName,UserPassword,nickname,sex,birth,UserEmail,phone,age,registerTime) values ('%s','%s','%s','%s','%s','%s','%s','%d','%s');" % (
            username, password, nickname, sex, birth, email, phone, age, registerTime)

        cursor.execute(sql)
        db.commit()
        re = Utils.responseGen(0, '注册成功', '')
        return re

    except Exception as e:
        db.rollback()
        re = Utils.responseGen(1, '注册失败', '')
        return re


#############################
def setVideoState(id, state):
    table = "video"
    sql = "UPDATE %s SET VideoStatus='%s' WHERE VideoID='%s'" % (table, state, id)
    cursor.execute(sql)
    db.commit()


def getUploadRecord(username):
    tableName = 'video'

    sql = "select VideoID,VideoName, VideoSize ,VideoUploadTime from %s where VideoUploaderName='%s'" % (
        tableName, username)

    cursor.execute(sql)

    listAll = cursor.fetchall()  # fetchall() 获取所有记录
    recordlist = []
    i = 1
    for item in listAll:
        job = {
            'key': i,
            'id': item[0],
            'name': item[1],
            'size': Utils.size_format(item[2]),
            'datetime': str(item[3])
        }
        i = i + 1
        recordlist.append(job)

    json_str = json.dumps(recordlist)

    return json_str


def getContentList(username):
    tableName = 'video'

    sql = "select * from %s where VideoUploaderName='%s'" % (
        tableName, username)

    cursor.execute(sql)

    listAll = cursor.fetchall()  # fetchall() 获取所有记录
    recordlist = []
    i = 1
    for item in listAll:
        job = {
            'key': i,
            'id': item[0],
            'icon': 'http://127.0.0.1:5000/api/pic/' + item[0],
            'name': item[1],
            'type': item[2],
            'timeLength': item[13],
            # 'size': Utils.size_format(item[3]),
            'size': item[3],
            'uploadTime': str(item[9]),
            'state': item[7]
        }
        i = i + 1
        recordlist.append(job)

    json_str = json.dumps(recordlist)

    return json_str


def getVideoList():
    tableName = 'video'

    sql = "select * from %s " % (
        tableName)

    cursor.execute(sql)

    listAll = cursor.fetchall()  # fetchall() 获取所有记录
    recordlist = []
    i = 1
    for item in listAll:
        job = {
            'key': i,
            'id': item[0],
            'icon': 'http://127.0.0.1:5000/api/pic/' + item[0],
            'name': item[1],
            'type': item[2],
            'timeLength': item[13],
            # 'size': Utils.size_format(item[3]),
            'size': item[3],
            'uploadTime': str(item[9]),
            'auth': item[8],
            'state': item[7]
        }
        i = i + 1
        recordlist.append(job)

    json_str = json.dumps(recordlist)

    return json_str


# 获取所有的特征库的字典数据
def getFeature():
    tableName = "feature"
    sql = "select FeatureID,FeatureArgs from %s " % (
        tableName)
    cursor.execute(sql)
    listAll = cursor.fetchall()  # fetchall() 获取所有记录
    dic = {}
    for item in listAll:
        # item[0]  # id
        # item[1]  # feature_dic的文本形式，用json就行
        dic[item[0]] = json.loads(item[1])
    return dic


# 保存特征数组的时间序列
def saveFeature(id, feature_dic):
    js = json.dumps(feature_dic)
    time = Utils.time_format()
    sql = "insert into Feature( FeatureID,FeatureTime,FeatureArgs) values ('%s','%s','%s' )" % (
        id, time, js)
    cursor.execute(sql)
    db.commit()


def setCopy(videoID, copyVideoID, copyScore, startTime, endTime, cStartTime, cEndTime):
    sql = "insert into Copy(videoID, copyVideoID, copyScore, startTime, endTime, cStartTime, cEndTime) values ('%s','%s','%s','%s','%s','%s','%s')" % (
        videoID, copyVideoID, str(copyScore), startTime, endTime, cStartTime, cEndTime)
    # print(sql)
    cursor.execute(sql)
    db.commit()


def addFileRecord(id, username, filename, filetype, size, path, FPS, timeLength):
    md5 = Utils.get_file_md5(path)
    time = Utils.time_format()

    sql = "insert into Video(VideoID,VideoName,VideoType,VideoSize,VideoMd5,VideoStatus,VideoUploaderName,VideoUploadTime,FPS,timeLength) values ('%s','%s','%s',%s,'%s','%s','%s','%s',%s,'%s');" % (
        id, filename, filetype, size, md5, '审核中', username, time, str(FPS), timeLength)
    cursor.execute(sql)
    db.commit()


def MD5_To_ID(md5):
    tableName = 'video'
    sql = " select VideoID from %s where VideoMd5='%s'" % (tableName, md5);
    cursor.execute(sql)
    listAll = cursor.fetchall()  # fetchall() 获取所有记录
    videoID = listAll[0][0]
    return videoID


def getVideoContent(id):
    video = getVideo(id)
    copyinfo = getCopyInfo(id)
    history = getHistory(id)
    data = {
        'video': video,
        'copyinfo': copyinfo,
        'history': history
    }
    return Utils.responseGen(0, 'success', data)


def getHistory(id):
    new_db = newConnection()
    new_cursor = new_db.cursor()
    sql = "select * from history where videoID = '%s'" % (id)
    new_cursor.execute(sql)
    records = new_cursor.fetchall()
    new_db.close()
    res = []
    for re in records:
        his = {
            'historyid': re[0],
            'videoid': re[1],
            'type': int(re[2]),
            'time': str(re[3]),
            'description': re[4],
            'operator': re[5],
            'state': re[6],
        }
        res.append(his)
    return res


def getCopyInfo(id):
    new_db = newConnection()
    new_cursor = new_db.cursor()
    tableName = 'copy'

    sql = "select * from %s where VideoID='%s'" % (
        tableName, id)

    new_cursor.execute(sql)
    record = new_cursor.fetchone()
    copyinfo = {}
    new_db.close()
    if record != None:
        copyinfo = getVideo(record[1])
        copyinfo['score'] = record[2]
        copyinfo['startTime'] = record[3]
        copyinfo['endTime'] = record[4]
        copyinfo['cStartTime'] = record[5]
        copyinfo['cEndTime'] = record[6]
    return copyinfo


# 根据id获取一个video实例
def getVideo(id):
    new_db = newConnection()
    new_cursor = new_db.cursor()
    tableName = 'video'

    sql = "select * from %s where VideoID='%s'" % (
        tableName, id)

    new_cursor.execute(sql)

    record = new_cursor.fetchone()  # fetchall() 获取所有记录
    new_db.close()
    video = {
        'id': record[0],
        'icon': 'http://127.0.0.1:5000/api/pic/' + record[0],
        'videoname': record[1],
        'type': record[2],
        'size': record[3],
        'md5': record[6],
        'status': record[7],
        'authName': record[8],
        'uploadtime': str(record[9]),
        'fps': record[12],
        'timeLength': record[13],
        'appealed': record[14],
    }
    return video


def deleteVideoRecord(id):
    # SQL 删除语句
    sql = "DELETE FROM Video WHERE VideoID='%s'" % (id)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()


def getUserDashboard(username):
    sql1 = "select nickname from user where username = '%s' ;" % (username)
    cursor.execute(sql1)
    record = cursor.fetchone()
    nickname = record[0]

    resbody = {
        'nickname': nickname
    }
    re = Utils.responseGen(0, 'success', resbody)
    return re


def getNoticeList():
    sql = "select * from notice"
    cursor.execute(sql)
    record = cursor.fetchall()
    notices = []
    for n in record:
        notice = {
            'id': n[0],
            'key': n[0],
            'content': n[1],
            'time': str(n[2]),
            'publisher': n[3],
            'title': n[4]
        }
        notices.append(notice)
        print(n)

    resbody = {'notices': notices}

    re = Utils.responseGen(0, 'success', resbody)
    return re


# 获取用户信息
def getUser(username):
    sql = "select * from user where UserName = '%s'" % (username)
    cursor.execute(sql)
    record = cursor.fetchone()
    user = {
        'username': record[0],
        'password': record[1],
        'avatar': record[11],
        'email': record[2],
        'age': record[3],
        'sex': record[4],
        'admined': record[6],
        'nickname': record[7],
        'birth': datetime.datetime.strftime(record[8], '%Y-%m-%d'),
        'phone': record[9],
        'sign': record[10],
        'registerTime': str(record[12])
    }

    res = Utils.responseGen(0, 'success', user)
    return res


# 更新用户信息
def updateUser(username, data):
    try:
        user = json.loads(data)
        nickname = user.get('nickname')
        sex = user.get('sex')
        age = user.get('age')
        birth = user.get('birth')
        email = user.get('email')
        phone = user.get('phone')
        sign = user.get('sign')
        sql = "update user set nickname = '%s', sex='%s' , age = '%d',birth = '%s',UserEmail='%s',phone='%s',sign='%s' where UserName = '%s'" % (
            nickname, sex, age, birth, email, phone, sign, username)
        print(sql)
        cursor.execute(sql)
        db.commit()
        res = Utils.responseGen(0, '更新成功！', '')
        return res
    except Exception as e:
        db.rollback()
        re = Utils.responseGen(1, '注册失败！', '')
        return re


# 查找用户
def fetchUser(keyword):
    sql = "SELECT UserName FROM user WHERE username REGEXP '%s';" % (keyword)

    cursor.execute(sql)
    record = cursor.fetchall()
    re = []
    for un in record:
        tmp = {
            'text': un[0],
            'value': un[0]
        }
        re.append(tmp)
    res = Utils.responseGen(0, '查找成功', re)
    return res


# 发送站内信息
def sendMessage(msgData):
    try:
        msg = json.loads(msgData)
        mFrom = msg.get('mFrom')
        mTo = msg.get('mTo')
        content = msg.get('content')
        subject = msg.get('subject')
        time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        for to in mTo:
            print(to)
            sql = "INSERT INTO message (`mFrom`,`mTo`,`content`,`sendTime`,`readed`,`subject`) VALUES ('%s','%s','%s','%s',0,'%s');" % (
                mFrom, to, content, time, subject)
            cursor.execute(sql)
            db.commit()
        res = Utils.responseGen(0, '发送成功！', '')
        return res
    except Exception as e:
        db.rollback()
        re = Utils.responseGen(1, '发送失败！', '')
        return re


# 获取消息列表
def getMessageList(username):
    sql = "select * from message where mTo = '%s' order by readed , sendTime desc" % (username)
    cursor.execute(sql)
    lists = cursor.fetchall()
    re = []
    for m in lists:
        msg = {
            'id': m[0],
            'key': m[0],
            'mFrom': m[1],
            'mTo': m[2],
            'content': m[3],
            'time': datetime.datetime.strftime(m[4], '%Y-%m-%d %H:%M:%S'),
            'readed': m[5],
            'subject': m[6]
        }
        re.append(msg)
    res = Utils.responseGen(0, "获取成功", re)
    return res


def setMessageState(data):
    try:
        id = int(data.get('id'))
        state = int(data.get('state'))
        sql = "update message set readed = '%d' where id = '%d'" % (state, id)
        cursor.execute(sql)
        db.commit()
        res = Utils.responseGen(0, "设置成功", '')
        return res
    except Exception as e:
        db.rollback()
        re = Utils.responseGen(1, "已读失败", '')
        return re


def getUnreadCount(username):
    new_db = newConnection()
    new_cursor = new_db.cursor()
    sql = " select count(*) from message where mTo = '%s' and readed=0" % (username)
    new_cursor.execute(sql)
    record = new_cursor.fetchone()
    count = record[0]
    new_db.close()
    re = Utils.responseGen(0, "获取成功！", count)
    return re


def deleteMessage(id):
    try:
        sql = "delete from message where id = '%d'" % (id)
        cursor.execute(sql)
        db.commit()
        re = Utils.responseGen(0, "删除成功", '')
        return re
    except Exception as e:
        db.rollback()
        res = Utils.responseGen(1, '删除失败', '')
        return res


def deleteUser(username):
    try:
        sql = "delete from user where username = '%s'" % (username)
        cursor.execute(sql)
        db.commit()
        re = Utils.responseGen(0, "删除成功", '')
        return re
    except Exception as e:
        res = Utils.responseGen(1, '删除失败', '')
        return res


def resetPassword(username):
    try:
        password = 'e291b62d1334ae32278a75a8038047e3'
        sql = "update user set userpassword = '%s' where username = '%s'" % (password, username)
        cursor.execute(sql)
        db.commit()
        re = Utils.responseGen(0, "重置成功", '')
        return re
    except Exception as e:
        db.rollback()
        res = Utils.responseGen(1, '重置失败', '')
        return res


def changePassword(data):
    try:
        password = data.get('password')
        username = data.get('username')
        sql = "update user set userpassword = '%s' where username = '%s'" % (password, username)
        cursor.execute(sql)
        db.commit()
        re = Utils.responseGen(0, "修改成功", '')
        return re
    except Exception as e:
        db.rollback()
        res = Utils.responseGen(1, '修改失败', '')
        return res


def setAuth(data):
    try:
        username = data.get('username')
        authPassword = data.get('authPassword')
        admined = data.get('auth')
        if (authPassword != 'BigChuang2020'):
            res = Utils.responseGen(1, '授权码错误,修改失败', '')
            return res
        print()
        sql = "update user set admined = '%d' where username = '%s'" % (admined, username)
        cursor.execute(sql)
        db.commit()
        re = Utils.responseGen(0, "修改成功", '')
        return re
    except Exception as e:
        db.rollback()
        res = Utils.responseGen(1, '修改失败', '')
        return res


def getFailedVideoList(username):
    new_db = newConnection()
    new_cursor = new_db.cursor();
    sql = "select * from video where videostatus = '不通过' and appealed=0 and videouploadername='%s'" % (username)
    new_cursor.execute(sql)
    records = new_cursor.fetchall()
    new_db.close()
    list = []
    key = 0
    for re in records:
        id = re[0]
        video = getVideo(id)
        copyinfo = getCopyInfo(id)
        data = {
            'key': key,
            'tag': '不通过',
            'name': re[1],
            'time': str(re[9]),
            'video': video,
            'copyinfo': copyinfo
        }
        list.append(data)
        key = key + 1

    res = Utils.responseGen(0, 'success', list)
    return res


def addHistory(videoid, type, time, description, operator, state):
    try:
        ndb = newConnection()
        ncursor = ndb.cursor()
        template_history = "insert into history(`videoid`,`type`,`time`,`description`,`operator`,`state`) values ('%s','%d','%s','%s','%s','%s')" % (
            videoid, type, time, description, operator, state)
        print(template_history)
        ncursor.execute(template_history)
        ndb.commit()
        ndb.close()
    except Exception as e:
        ndb.rollback()
        ndb.close()


def updateHistory(videoid, type, time, description, operator, state):
    try:
        new_db = newConnection()
        new_cursor = new_db.cursor()
        sql = "update history set time='%s',description='%s',operator='%s',state='%s' where videoid = '%s' and type = '%s'" % (
            time, description, operator, state, videoid, type)
        new_cursor.execute(sql)
        new_db.commit()
        new_db.close()
    except Exception as e:
        new_db.rollback()
        new_db.close()


def addNewAppeal(data, username):
    template_appeal = 'insert into appeal(`videoid`,`appealTime`,`appealername`,`appealContent`,`state`) values(%s,%s,%s,%s,1)'
    template_video = 'update video set appealed = 1 where videoid = %s'
    template_history = "insert into history(`videoid`,`type`,`time`,`description`,`operator`,`state`) values (%s,4,%s,'申诉申请成功',%s,1)"
    data_appeal = []
    data_video = []
    data_history = []
    try:
        for re in data:
            selected = re.get('selected')
            if selected:
                id = re.get('id')
                appeal = re.get('appeal')
                time = Utils.time_format()
                data_appeal.append((id, time, username, appeal))
                data_video.append((id,))
                data_history.append((id, time, username))
        cursor.executemany(template_appeal, data_appeal)
        cursor.executemany(template_video, data_video)
        cursor.executemany(template_history, data_history)
        db.commit()
        return Utils.responseGen(0, '申诉已提交', '')
    except Exception as e:
        db.rollback()
        res = Utils.responseGen(1, '申诉失败', '')
        return res


def getAppealList(username, type, all=False):
    new_db = newConnection()
    new_cursor = new_db.cursor()
    sql = ''
    if all == True:
        if type == 0:
            # 全部
            sql = "select * from appeal "
        elif type == 1:
            # 进行中
            sql = "select * from appeal where  state=1"
        elif type == 2:
            # 完成
            sql = "select * from appeal where  state=2"
    else:
        if type == 0:
            # 全部
            sql = "select * from appeal where appealerName='%s'" % (username)
        elif type == 1:
            # 进行中
            sql = "select * from appeal where appealerName='%s' and state=1" % (username)
        elif type == 2:
            # 完成
            sql = "select * from appeal where appealerName='%s' and state=2" % (username)
    new_cursor.execute(sql)
    record = new_cursor.fetchall()
    new_db.close()
    res = []
    for re in record:
        appeal = {
            'appealID': re[0],
            'videoID': re[1],
            'appealTime': str(re[2]),
            'appealerName': re[3],
            'appealContent': re[4],
            'state': re[5],
            'appealResult': re[6],
            'resolver': re[7],
            'resolveTime': str(re[8]),
            'appealFeedback': re[9]}
        video = getVideo(re[1])
        r = {
            'key': re[0],
            'appeal': appeal,
            'video': video
        }
        res.append(r)
    return Utils.responseGen(0, 'success', res)


def getAppealCount(username, all=False):
    new_db = newConnection()
    new_cursor = new_db.cursor()
    sql1 = ''
    sql2 = ''
    sql3 = ''
    if all:
        # 全部
        sql1 = "select count(*) from appeal "
        # 进行中
        sql2 = "select count(*) from appeal where  state=1"
        # 完成
        sql3 = "select count(*) from appeal where  state=2"
    else:
        # 全部
        sql1 = "select count(*) from appeal where appealerName='%s'" % (username)
        # 进行中
        sql2 = "select count(*) from appeal where appealerName='%s' and state=1" % (username)
        # 完成
        sql3 = "select count(*) from appeal where appealerName='%s' and state=2" % (username)

    # 全部
    new_cursor.execute(sql1)
    c_all = new_cursor.fetchone()[0]
    # 进行中
    new_cursor.execute(sql2)
    c_process = new_cursor.fetchone()[0]
    # 已完成
    new_cursor.execute(sql3)
    c_finish = new_cursor.fetchone()[0]

    new_db.close()
    res = {
        'all': c_all,
        'finish': c_finish,
        'process': c_process
    }
    return Utils.responseGen(0, 'success', res)


def getAppealDetail(id):
    video = getVideo(id)
    copyinfo = getCopyInfo(id)
    sql = "select * from appeal where videoid = '%s' " % (id)
    cursor.execute(sql)
    re = cursor.fetchone()

    appeal = {
        'appealID': re[0],
        'videoID': re[1],
        'appealTime': str(re[2]),
        'appealerName': re[3],
        'appealContent': re[4],
        'state': re[5],
        'appealResult': re[6],
        'resolver': re[7],
        'resolveTime': str(re[8]),
        'appealFeedback': re[9]}
    data = {
        'appeal': appeal,
        'video': video,
        'copyinfo': copyinfo
    }
    return Utils.responseGen(0, 'success', data)


def resolveAppeal(data):
    try:
        id = data.get('id')
        appealResult = int(data.get('appealResult'))
        appealFeedback = data.get('appealFeedback')
        resolver = data.get('resolver')
        resolveTime = data.get('resolveTime')
        type = data.get('type')
        sql = "update appeal set appealResult = '%s',appealFeedback = '%s',state=2, resolver='%s',resolveTime='%s' where videoID='%s'" % (
            appealResult, appealFeedback, resolver, resolveTime, id)
        cursor.execute(sql)
        db.commit()
        status = '不通过' if appealResult == 0 else '审核通过'
        sql = "update video set videostatus='%s' where videoID = '%s'" % (status, id)
        cursor.execute(sql)
        db.commit()
        print(type)
        if type == 0:
            addHistory(id, 5, resolveTime, '申诉已完成', resolver, appealResult)
        else:
            updateHistory(id, 5, resolveTime, '申诉已完成', resolver, appealResult)
        return Utils.responseGen(0, 'success', '')
    except Exception as e:
        return Utils.responseGen(1, 'fail', '')


def deleteNotice(id):
    try:
        sql = "delete from notice where id='%s'" % (id)
        cursor.execute(sql)
        db.commit()
        return Utils.responseGen(0, '删除成功', '')
    except Exception as e:
        db.rollback()
        return Utils.responseGen(1, '删除失败', '')


def newNotice(data):
    try:
        content = data.get('content')
        publisher = data.get('publisher')
        title = data.get('title')
        time = Utils.time_format()
        sql = "insert into notice (title,time,publisher,content) values ('%s','%s','%s','%s')" % (
            title, time, publisher, content)
        cursor.execute(sql)
        db.commit()
        return Utils.responseGen(0, '发布成功', '')
    except Exception as e:
        db.rollback()
        return Utils.responseGen(1, '发布失败', '')


def updateNotice(data):
    try:
        content = data.get('content')
        publisher = data.get('publisher')
        title = data.get('title')
        time = data.get('time')
        id = data.get('id')
        sql = "update notice set content='%s',publisher='%s',title='%s',time='%s' where id ='%s'" % (content, publisher,
                                                                                                     title, time, id)
        print(sql)
        cursor.execute(sql)
        db.commit()
        return Utils.responseGen(0, '发布成功', '')
    except Exception as e:
        db.rollback()
        return Utils.responseGen(1, '发布失败', '')


def getFeedbackList():
    sql = 'select * from feedback'
    cursor.execute(sql)
    records = cursor.fetchall()
    data = []
    for re in records:
        feedback = {
            'key':re[0],
            'id': re[0],
            'title': re[1],
            'content': re[2],
            'smtPerson': re[3],
            'applied': re[4],
            'applier': re[5],
            'applyContent': re[6],
            'smtTime': str(re[7]),
            'applyTime': str(re[8]),
            'readed': str(re[9])
        }
        data.append(feedback)
    return Utils.responseGen(0, 'success', data)


def newFeedback(data):
    try:
        title = data.get('title')
        content = data.get('content')
        smtPerson = data.get('smtPerson')
        smtTime = Utils.time_format()
        sql = "insert into feedback(title,content,smtPerson,smtTime) values ('%s','%s','%s','%s')" % (
            title, content, smtPerson, smtTime)
        cursor.execute(sql)
        db.commit()
        return Utils.responseGen(0, 'success', '')
    except Exception as e:
        db.rollback()
        return Utils.responseGen(1, '提交失败', '')


def replyFeedback(data):
    try:
        id = data.get('id')
        applyTime = Utils.time_format()
        applier = data.get('applier')
        applyContent = data.get('applyContent')
        sql = "update feedback set applyTime='%s',applier='%s',applyContent='%s',applied=1,readed=1 where id='%s'" % (
            applyTime, applier, applyContent, id)
        cursor.execute(sql)
        db.commit()
        Utils.sendMessage_fedbkReply(id)
        return Utils.responseGen(0, 'success', '')
    except Exception as e:
        db.rollback()
        return Utils.responseGen(1, '回复失败', '')


def feedbackSetReaded(id):
    sql = "update feedback set readed=1 where id = '%s'" % (id)
    cursor.execute(sql)
    db.commit()
    return Utils.responseGen(0, 'success', '')
