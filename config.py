import os

Test = "Hello world"

# 运行模式
Debug = True

# 数据库配置
SQL_USERNAME = "root"
SQL_PSD = "090312"  # 本机mysql 连接密码

# 文件夹设置

# 所有上传的文件存储在upload文件夹中
# 安排检测任务时，产生的关键帧和特征存放在temp文件夹中
# 如果检测成功，则把相应的视频和特征移入特征库
# 若检测不成功，则保留视频于原文件夹


ROOT_FOLDER = os.getcwd() + '/data/'
UPLOAD_FOLDER = ROOT_FOLDER + "/Upload/"  # 用户上传文件存储文件夹,待检测
VIDEO_DATABASE = ROOT_FOLDER + "/VideoDB/video/"  # 视频库文件夹，里面存储的是视频文件
FEATURE_DATABASE = ROOT_FOLDER + "/VideoDB/feature/"  # 特征库文件夹，里面存储的是视频库中视频对应的特征文件
TMP_FOLDER = ROOT_FOLDER + "/DetectTmp/"  # 临时文件夹，用于处理当前任务视频的
PIC_FOLDER = ROOT_FOLDER + "/pic/"  # 存放图片文件夹
AVATAR_FOLDER = ROOT_FOLDER + "/avatar/"  # 存放用户头像的文件夹
PIC_TMP = ROOT_FOLDER + "/PicTmp/"  # 图片临时文件夹
# 允许并行处理的任务数
MAX_VIDEO_PROCESS = 5
