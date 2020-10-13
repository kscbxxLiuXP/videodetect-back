import os
import json
import shutil
import threading

import cv2

from app.controller import MySqlUtil as DBUtil
from app.controller import Utils
from app.controller import VideoDBManage
from app.models.TaskManager import taskManager
import config

upload_folder = config.UPLOAD_FOLDER
videoBase = config.VIDEO_DATABASE
featureBase = config.FEATURE_DATABASE
tmpFolder = config.TMP_FOLDER

base_path = os.path.abspath(os.path.dirname(__file__))


# 用户上传文件
def fileUpload(file, username):
    try:
        # 生成视频ID标识
        id = Utils.generate_timeID()
        # 获取文件类型
        filetype = getFileType(file.filename)
        # 重命名文件名并生成文件存储路径
        file_path = os.path.join(upload_folder, generateFileName(file.filename, id))
        file.save(file_path)
        # 导出缩略图
        camera = cv2.VideoCapture(file_path)
        res, image = camera.read()
        cv2.imwrite(config.PIC_FOLDER + id + '.jpg', image)
        camera.release()
        # 获取视频fps以及视频长度
        info = Utils.getVideoInfo(file_path)
        DBUtil.addFileRecord(id, username, file.filename, filetype, Utils.get_file_size(file_path), file_path,
                             info['fps'], info['length'])
        # 添加检测队列
        taskManager.addTask(id)
        DBUtil.addHistory(id, 1, Utils.time_format(), "上传成功", username, 1)

        return json.dumps({'code': 0})
    except Exception as e:
        print(str(e))
        return json.dumps({'code': -1, 'message': str(e)})


# 管理员添加版权库文件
def videoAdd(file, username):
    try:
        # 生成视频ID标识
        id = file.filename.split('.')[0]
        # 获取文件类型
        filetype = getFileType(file.filename)
        # 重命名文件名并生成文件存储路径
        file_path = os.path.join(upload_folder, file.filename)
        # 导出缩略图
        camera = cv2.VideoCapture(file_path)
        res, image = camera.read()
        cv2.imwrite(config.PIC_FOLDER + id + '.jpg', image)
        camera.release()
        # 获取视频fps以及视频长度
        info = Utils.getVideoInfo(file_path)
        DBUtil.addFileRecord(id, username, file.filename, filetype, Utils.get_file_size(file_path), file_path,
                             info['fps'], info['length'])
        task = threading.Thread(target=VideoDBManage.addVideo, args=(id,))
        task.start()
        return json.dumps({'code': 0})
    except Exception as e:
        print(str(e))
        return json.dumps({'code': -1, 'message': str(e)})


# 用户上传之后，想删除该次上传
def fileDeleteByMD5(md5):
    # 由MD5获取videoID
    id = DBUtil.MD5_To_ID(md5)
    result = fileDeleteByID(id)
    return Utils.responseGen(result, '', '')


def fileDeleteByID(id):
    try:
        # 获取Video实例
        # video = DBUtil.getVideo(id)
        # username = video.get('username')
        # filename = id + '.' + video.get('type')
        file_path = getVideoAddress(id)
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(file_path):
            return 1
        else:
            return 0
    except Exception as e:
        return 1


# 根据文件id生成文件名称
def generateFileName(filename, fileID):
    return fileID + '.' + getFileType(filename)


# 根据id获取视频的存储地址
def getVideoAddress(videoID):
    video = DBUtil.getVideo(videoID)
    status = video.get('status')
    address = getVideoDir(videoID) + videoID + "." + video.get('type')
    return address


# 根据id获取视频的文件夹
def getVideoDir(videoID):
    video = DBUtil.getVideo(videoID)
    status = video.get('status')
    address = ""
    if status != "审核通过":
        address = upload_folder
    else:
        address = videoBase
    return address


# 获取文件后缀
def getFileType(filename):
    suffix = filename.split('.')[1]
    return suffix


# 移动文件
def movefile(srcfile, dstfolder):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        spath, sname = os.path.split(srcfile)  # 分离文件名和路径
        dstfile = os.path.join(dstfolder, sname)
        shutil.move(srcfile, dstfile)  # 移动文件
