import os
import shutil

import config

import app.controller.FileUtil as FileUtil
import app.controller.MySqlUtil as DBUtil
from app.controller.algorithms.shotSegmentation import key_frame_extra
from app.controller.algorithms.ImageNNExtract import imageNNExtract
from app.controller.algorithms.video_retrieval import video_retrieval
from app.controller.algorithms.frequencyKeyFrame import frequency_extract


# 向版权库中增加视频
def addVideo(id):
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
    query_frame_2_time = frequency_extract(frequency=15, input_video=videoAddress, output_folder=videoFolder)
    print("关键帧提取完成")
    # 特征提取
    imageNNExtract(input_frame_folder=videoFolder, output_npy=featureAddress)
    print("特征提取完成")
    # 移动视频文件至版权库
    FileUtil.movefile(videoAddress, config.VIDEO_DATABASE)
    # 移动特征文件至版权库
    FileUtil.movefile(featureAddress + ".npy", config.FEATURE_DATABASE)
    # 删除临时文件夹
    shutil.rmtree(videoFolder)
    # 保存特征文件至数据库
    DBUtil.saveFeature(id, query_frame_2_time)
    # # 修改数据库状态为通过
    DBUtil.setVideoState(id, "审核通过")


if __name__ == "__main__":
    addVideo('1293730300')
    addVideo('417605300')
    addVideo('1234417600')
    addVideo('1243533500')
    addVideo('1244621900')
    addVideo('1244627000')
    addVideo('1260706600')
    addVideo('1293727100')
