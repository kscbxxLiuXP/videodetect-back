import os
import shutil

import config

import app.controller.FileUtil as FileUtil
import app.controller.MySqlUtil as DBUtil
from app.controller import Utils
from app.controller.algorithms.shotSegmentation import key_frame_extra
from app.controller.algorithms.frequencyKeyFrame import frequency_extract
from app.controller.algorithms.ImageNNExtract import imageNNExtract
from app.controller.algorithms.video_retrieval import video_retrieval


# 开始检测任务
def videoDetect(id):
    Utils.sendNotice_startDetect(id)
    DBUtil.addHistory(id, 2, Utils.time_format(), "系统开始审核", 'SYSTEM', 1)
    # 先在tmp目录中创建一个视频文件夹
    videoFolder = config.TMP_FOLDER + id  # D:/大创/项目代码/website/data/DetectTmp/20200516190604945088
    # print(videoFolder)
    if os.path.exists(videoFolder):
        print("已存在")
    else:
        os.mkdir(videoFolder)

    # 获取原视频文件
    videoAddress = FileUtil.getVideoAddress(id)  # D:/大创/项目代码/website/data/Upload/20200516190604945088.mp4
    # print(videoAddress)
    # print(videoFolder + "/" + id + ".npy")
    featureAddress = videoFolder + "/" + id  # D:/大创/项目代码/website/data/DetectTmp/20200516190604945088/20200516190604945088.npy
    # 提取关键帧
    query_frame_2_time = frequency_extract(frequency=10, input_video=videoAddress, output_folder=videoFolder)
    print("关键帧提取完成")
    # 特征提取
    imageNNExtract(input_frame_folder=videoFolder, output_npy=featureAddress)
    print("特征提取完成")
    # 匹配
    #
    #
    refer_frame_2_time = DBUtil.getFeature()
    copy_info = video_retrieval(featureAddress, config.FEATURE_DATABASE, query_frame_2_time, refer_frame_2_time)
    copyid = copy_info[1].split('.')[-2].split('/')[-1]
    score = copy_info[0]
    start_time = copy_info[2]
    end_time = copy_info[3]
    copy_start_time = copy_info[4]
    copy_end_time = copy_info[5]
    print("score:", score)
    print("copyid:", copyid)
    print("starttime:", start_time)
    print("endtime:", end_time)
    print("cstarttime:", copy_start_time)
    print("cendtime", copy_end_time)
    success = 0
    # 如果检测通过
    if success == 1:
        # 移动视频文件至版权库
        FileUtil.movefile(videoAddress, config.VIDEO_DATABASE)
        # 移动特征文件至版权库
        FileUtil.movefile(featureAddress + ".npy", config.FEATURE_DATABASE)
        # 删除临时文件夹
        shutil.rmtree(videoFolder)
        # 保存特征文件至数据库
        DBUtil.saveFeature(id, query_frame_2_time)
        # 修改数据库状态为通过
        DBUtil.setVideoState(id, "审核通过")
        DBUtil.addHistory(id, 3, Utils.time_format(), "检测完成", 'SYSTEM', 1)
    else:
        # 删除临时文件夹
        shutil.rmtree(videoFolder)
        # 修改数据库状态为不通过
        DBUtil.setVideoState(id, "不通过")
        # 建立拷贝信息
        DBUtil.setCopy(id, copyid, score, start_time, end_time, copy_start_time, copy_end_time)
        DBUtil.addHistory(id, 3, Utils.time_format(), "检测完成", 'SYSTEM', 0)
    Utils.sendNotice_finishDetect(id)


if __name__ == "__main__":
    id = '20200608172028834016'
    videoDetect(id)
