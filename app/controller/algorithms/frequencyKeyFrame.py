# frequency 每隔frequency帧数提取一帧
# path 视频文件
# to_path 关键帧保存路径 以 '/' 结尾
import os

import cv2

# 帧转化为对应时间
import config
from app.controller import FileUtil


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


def frequency_extract(frequency, input_video, output_folder):
    frameIndex = 1;
    outputIndex = 0;
    capture = cv2.VideoCapture(input_video)
    totalFrameNumber = capture.get(7);
    FPS = capture.get(5)  # 这个是获取视频帧率
    dic = {}
    while True:
        flag, frame = capture.read()
        if not flag:
            break
        # cv2.imshow('video', frame)
        if frameIndex % frequency == 0:
            newPath = output_folder + "/" + str(frameIndex) + ".jpg"
            cv2.imencode('.jpg', frame)[1].tofile(newPath)
            outputIndex += 1
            dic[outputIndex] = frames_to_timecode(FPS, frameIndex)
            print("\rprocess:[", str(frameIndex), '/', str(totalFrameNumber), ']', end='')
        frameIndex += 1
    return dic


if __name__ == "__main__":
    id = '1293730300'
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

    # 提取关键帧
    query_frame_2_time = frequency_extract(frequency=20, input_video=videoAddress, output_folder=videoFolder)
    print(query_frame_2_time)
    print("关键帧提取完成")
