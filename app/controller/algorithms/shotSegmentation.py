import time

import cv2
import numpy as np


class frame_info:
    def __init__(self, index, diff):
        self.index = index  # 帧编号
        self.diff = diff  # 当前帧与前一帧的diff


# 计算每一帧与前一帧的直方图的差
def cal_diff(input):
    capture = cv2.VideoCapture(input)
    totalFrameNumber = capture.get(7);  # 获取视频的总帧数
    list_frames = []
    frameIndex = 1
    flag, frame = capture.read()
    while flag:
        gray_current = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 该帧图形处理
        n_pixel_current = frame.shape[0] * frame.shape[1]
        hist_current = cv2.calcHist([gray_current], [0], None, [16], [0, 256])
        hist_current = hist_current * (1.0 / n_pixel_current)

        if frameIndex == 1:
            hist_pre = hist_current
        # # 前一帧图像处理
        # gray_pre = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # n_pixel_pre = frame.shape[0] * frame.shape[1]
        # hist_pre = cv2.calcHist([gray_pre], [0], None, [16], [0, 256])
        # hist_pre = hist_pre * (1.0 / n_pixel_pre)

        diff = np.sum(np.abs(np.subtract(hist_current, hist_pre)))
        list_frames.append(frame_info(frameIndex, diff))

        print("\rprocess:[", str(frameIndex), '/', str(totalFrameNumber), ']', end='')
        # time.sleep(0.0001)
        hist_pre = hist_current
        frameIndex += 1
        flag, frame = capture.read()
    return list_frames


def display_frame_info(frames):
    for frame_info in frames:
        print("index: " + str(frame_info.index) + "\tdiff:" + str(frame_info.diff))


# 进行边缘检测
# 找寻差值最大的帧
'''
1、创建一个窗口，定义窗口中帧的数量，每次对窗口中的帧进行判断。然后取对应数量的帧；
2、计算窗口中差值最大的帧，定义为可疑的镜头边缘帧M再进行下一步判断；
3、取得前一镜头边缘帧P，判断当前M与P中间的帧数量，是否超过设定的镜头最小帧数阈值，如果不超过，则舍弃M，清空窗口数据，进行下一个镜头判断；否则进行下一步判断；
4、判断M的差值是不是P到M的平均差值(不包括M的差值)的一个阈值倍数。
'''


def second_find_diff_max(list_frames=[], start_no=0):
    sus_max_frame = []  # 可疑的镜头帧，以M为值
    window_frame = []
    m_MinLengthOfShot = 8
    m_suddenJudge = 2

    # window_size设定窗口内存放帧的个数
    window_size = 10

    length = len(list_frames)
    index_list = range(0, length)
    for index in index_list:
        frame_item = list_frames[index]
        window_frame.append(frame_item)

        if len(window_frame) < window_size:
            continue

        # 处理窗口帧的判断
        max_diff_frame = getMaxFrame(window_frame)
        max_diff_index = max_diff_frame.index

        if len(sus_max_frame) == 0:
            sus_max_frame.append(max_diff_frame)
            continue
        last_max_frame = sus_max_frame[-1]

        '''
            判断是否超过镜头跨度最小值
            1、低于，则移除窗口中最大帧之前的所有帧(包括最大帧)，然后重新移动窗口
            2、则进入下一步判断
        '''
        if (max_diff_index - last_max_frame.index) < m_MinLengthOfShot:
            start_index = window_frame[0].index
            if last_max_frame.diff < max_diff_frame.diff:
                #  最后一条可疑frame失效
                sus_max_frame.pop(-1)
                sus_max_frame.append(max_diff_frame)
                pop_count = max_diff_index - start_index + 1
            else:
                #  舍弃当前的可疑frame，整个窗口清除
                pop_count = window_size

            count = 0
            while True:
                window_frame.pop(0)
                count += 1
                if count >= pop_count:
                    break
            continue

        '''
            镜头差超过最小镜头值后的下一步判断，判断是否为可疑帧
            当前最大帧距离上一个可疑帧的平均差值是否差距很大
        '''
        sum_start_index = last_max_frame.index + 1 - start_no
        sum_end_index = max_diff_index - 1 - start_no
        id_no = sum_start_index
        # print("{0}, {1}, {2}".format(sum_start_index, sum_end_index, id_no))
        sum_diff = 0
        while True:

            sum_frame_item = list_frames[id_no]
            sum_diff += sum_frame_item.diff
            id_no += 1
            if id_no > sum_end_index:
                break

        average_diff = sum_diff / (sum_end_index - sum_start_index + 1)
        if max_diff_frame.diff >= (m_suddenJudge * average_diff):
            sus_max_frame.append(max_diff_frame)

        window_frame = []
        continue

    sus_last_frame = sus_max_frame[-1]
    last_frame = list_frames[-1]
    if sus_last_frame.index < last_frame.index:
        sus_max_frame.append(last_frame)

    return sus_max_frame


# 取窗口中的最大帧
def getMaxFrame(window_frame):
    max_frame = window_frame[0]
    for frame_info in window_frame:
        if frame_info.diff > max_frame.diff:
            max_frame = frame_info
    return max_frame


def third_optimize_frame(tag_frames, all_frames, start_no):
    '''
        进一步优化
        对于每一个分割镜头帧，其前后的帧的平均值都远远低于其
    '''
    # config
    new_tag_frames = []
    m_offset_frame_count = 4
    m_offset = 4
    m_diff_threshold = 6
    m_optimize_steep = 2
    m_optimize = 2

    for tag_frame in tag_frames:

        tag_index = tag_frame.index

        if tag_frame.diff < m_diff_threshold:
            continue

        #  向前取m_MinLengthOfShot个帧
        pre_start_index = tag_index - m_offset_frame_count - m_offset
        pre_start_no = pre_start_index - start_no
        if pre_start_no < 0:
            #  如果往前找时已经到头了，则认为此镜头不可取，将镜头交给最起始的帧
            new_tag_frames.append(all_frames[0])
            continue
        pre_end_no = tag_index - 1 - start_no - m_offset

        pre_sum_diff = 0
        emulator_no = pre_start_no
        while True:
            pre_frame_info = all_frames[emulator_no]
            pre_sum_diff += pre_frame_info.diff
            emulator_no += 1
            if tag_frame.index == 42230:
                print("向前：{0}, {1}".format(pre_frame_info.index, pre_frame_info.diff))
            if emulator_no > pre_end_no:
                break

        #  向后取m_MinLengthOfShot个帧
        back_end_index = tag_index + m_offset_frame_count + m_offset
        back_end_no = back_end_index - start_no
        if back_end_no >= len(all_frames):
            #  如果往后找时已经到头了，则认为此镜头不可取，将镜头交给结束的帧
            new_tag_frames.append(all_frames[-1])
            continue
        back_start_no = tag_index + 1 - start_no + m_offset

        back_sum_diff = 0
        emulator_no = back_start_no
        while True:
            back_frame_info = all_frames[emulator_no]
            back_sum_diff += back_frame_info.diff
            emulator_no += 1
            if emulator_no > back_end_no:
                break

        is_steep = False
        # 判断是不是陡增/或者陡降
        pre_average_diff = pre_sum_diff / m_offset_frame_count
        print("前平均 {0}, {1}, {2}".format(tag_frame.index, tag_frame.diff, pre_average_diff))
        if tag_frame.diff > (m_optimize_steep * pre_average_diff):
            is_steep = True

        back_average_diff = back_sum_diff / m_offset_frame_count
        print("后平均 {0}, {1}, {2}".format(tag_frame.index, tag_frame.diff, back_average_diff))
        if tag_frame.diff > (m_optimize_steep * back_average_diff):
            is_steep = True

        # 计算平均值，如果大于一定的阈值倍数，则认可，不然舍弃
        sum_diff = pre_sum_diff + back_sum_diff
        average_diff = sum_diff / (m_offset_frame_count * 2)
        print("{0}, {1}, {2}".format(tag_frame.index, tag_frame.diff, average_diff))
        if tag_frame.diff > (m_optimize * average_diff) or is_steep:
            new_tag_frames.append(tag_frame)

    return new_tag_frames


# 导出每一个镜头的关键帧
def export_frames(frames, input, output_folder):
    frameIndex = 1;
    outputIndex = 0;
    capture = cv2.VideoCapture(input)

    FPS = capture.get(5)  # 这个是获取视频帧率
    dic = {}
    while True:
        flag, frame = capture.read()
        if not flag:
            break
        # cv2.imshow('video', frame)
        if frames[outputIndex].index == frameIndex:
            newPath = output_folder + "/" + str(frameIndex) + ".jpg"
            cv2.imencode('.jpg', frame)[1].tofile(newPath)
            outputIndex += 1
            dic[outputIndex] = frames_to_timecode(FPS, frameIndex)
        frameIndex += 1
    return dic


# 帧转化为对应时间
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


def key_frame_extra(input_video, output_folder):
    list_frames = cal_diff(input_video)
    final_frames = second_find_diff_max(list_frames=list_frames)
    dic = export_frames(final_frames, input_video, output_folder)
    return dic
