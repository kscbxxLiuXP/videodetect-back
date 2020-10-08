import threading
import time
from queue import Queue

import config

Max = config.MAX_VIDEO_PROCESS


class TaskManager(threading.Thread):
    # 用队列保存所有待检测任务，如果没有达到最大处理数，就不断取出，达到后等待
    taskQueue = Queue()

    def __init__(self, n):
        super(TaskManager, self).__init__()  # 重构run函数必须要写
        self.number = n

    def test(self):
        self.number += 1
        print("test taskManager " + str(self.number))

    def addTask(self, videoID):
        task = threading.Thread(target=self.videoDetect, args=(videoID,))
        self.taskQueue.put(task)

    def run(self):
        print('\033[1;35m TaskManager is Monitoring  \033[0m!')
        while True:
            # sleep(1)防止while true过度占用CPU资源导致CPU占用率100%而暴毙
            time.sleep(2)
            if self.number <= Max and not self.taskQueue.empty():
                task = self.taskQueue.get()
                task.start()
                self.number += 1

    def videoDetect(self, videoID):
        from app.controller.algorithms.VideoDetect import videoDetect
        print('\033[1;35m VideoDetection run for ' + str(videoID) + '  \033[0m')
        time.sleep(10)
        videoDetect(videoID)
        print('\033[1;32m VideoDetection finish for ' + str(videoID) + '  \033[0m')
        self.number += -1


# 单线程监控任务管理，使用单例模式运行
taskManager = TaskManager(0)
