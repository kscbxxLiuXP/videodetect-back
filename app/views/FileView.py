from flask import Blueprint, request, send_from_directory, Response
import json
from app.controller import MySqlUtil as DBUtil, Utils
from app.controller import FileUtil
import config

FileBlue = Blueprint("fileBlue", __name__)


# 用户上传文件
@FileBlue.route('/fileUpload/<username>', methods=['POST'])
def fileUpload(username):
    f = request.files["file"]
    return FileUtil.fileUpload(f, username)


# 管理员增加视频库
@FileBlue.route('/videoAdd/<username>', methods=['POST'])
def videoAdd(username):
    f = request.files["file"]
    return FileUtil.videoAdd(f, username)


# 根据文件的MD5值删除文件
@FileBlue.route('/fileDeleteByMD5/md5/<md5>', methods=['GET'])
def fileDeleteByMD5(md5):
    return FileUtil.fileDeleteByMD5(md5)


# 根据文件的id值删除视频文件
@FileBlue.route('/fileDelete/id/<id>', methods=['GET'])
def fileDeleteByID(id):
    a = FileUtil.fileDeleteByID(id)
    # 删除对应记录
    b = DBUtil.deleteVideoRecord(id)
    result = 0 if (a == 0 and b == 0) else 1
    return Utils.responseGen(result, '', '')


@FileBlue.route('/deleteFile/<id>')
def deleteFile(id):
    result = deleteFiles(id)
    return Utils.responseGen(result, '', '')


def deleteFiles(id):
    a = FileUtil.fileDeleteByID(id)
    # 删除对应记录
    b = DBUtil.deleteVideoRecord(id)
    result = 0 if (a == 0 and b == 0) else 1
    return result


@FileBlue.route('/deleteManyFile', methods=['POST'])
def deleteManyFile(id):
    data = json.loads(request.get_data(as_text=True))
    failed = []
    for video in data:
        id = video.get('id')
        name = video.get('name')
        result = deleteFiles(id)
        if result != 0:
            failed.append(name)
    if failed.__len__() == 0:
        return Utils.responseGen(0, '删除成功', '')
    else:
        return Utils.responseGen(1, '删除失败', failed)


# 返回一个video的json对象
@FileBlue.route('/getVideoContent/<id>')
def getVideoContent(id):
    return DBUtil.getVideoContent(id)


# 校验MD5值
@FileBlue.route('/checkFileMD5/<md5>')
def checkFileMD5(md5):
    tmp = DBUtil.checkFileMD5(md5)
    re = {'code': tmp}
    return json.dumps(re)


# 返回一个视频文件
@FileBlue.route('/fileGet/<id>', methods=['GET'])
def fileGet(id):
    # video = DBUtil.getVideo(id)
    path = FileUtil.getVideoDir(id)
    name = id + '.mp4'
    # 参数as_attachment=True，否则对于图片格式、txt格式，会把文件内容直接显示在浏览器，对于xlsx等格式，虽然会下载，但是下载的文件名也不正确
    return send_from_directory(path, name, as_attachment=True)


# 返回图片
@FileBlue.route('/pic/<id>')
def pic(id):
    with open(config.PIC_FOLDER + id + '.jpg', 'rb') as f:
        image = f.read()
    resp = Response(image, mimetype="image/jpeg")
    return resp


# 给用户id返回头像，因为需要知道用户有没有上传头像，需要从数据库读该用户是否使用默认头像
@FileBlue.route('/getAvatar/<userid>')
def getAvatar(userid):
    new_db = DBUtil.newConnection()
    new_cursor = new_db.cursor()
    sql = "select avatar from user where username = '%s'" % (userid)
    new_cursor.execute(sql)
    record = new_cursor.fetchone()
    new_db.close()
    filename = record[0]
    return avatar(filename)


# 已知用户头像的文件id直接读取
@FileBlue.route('/avatar/<id>')
def avatar(id):
    with open(config.AVATAR_FOLDER + id + '.jpg', 'rb') as f:
        image = f.read()
    resp = Response(image, mimetype="image/jpeg")
    return resp


@FileBlue.route('/avatar/upload/<username>', methods=['POST'])
def avatarUpload(username):
    f = request.files["file"]
    return FileUtil.avatarUpload(f, username)


@FileBlue.route('/tmpPic/<id>')
def tmpPic(id):
    with open(config.PIC_TMP + id + '.jpg', 'rb') as f:
        image = f.read()
    resp = Response(image, mimetype="image/jpeg")
    return resp


@FileBlue.route('/confirmAvatarChange/<username>')
def confirmAvatarChange(username):
    return FileUtil.confirmAvatarChange(username)


@FileBlue.route('/cancelAvatarChange/<username>')
def cancelAvatarChange(username):
    return FileUtil.cancelAvatarChange(username)
