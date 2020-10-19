## 一、运行环境

- Python 3.6 及以上
- Pip
- MySQL

## 二.项目依赖

### 1.Flask

运行 `pip install flask`

### 2.MySQLDB

运行 `pip install mysql`
后期可能会考虑使用sqlalchemy来代替

### 3.opencv

`pip install opencv-python`

若安装失败，先将pip工具更新

### 4.pytorch

前往 https://pytorch.org/get-started/locally/ 官网下载

选择pip,CUDA选择None,

复制pip安装命令在命令行中运行

### 5.flask_cors

​    运行 `pip install flask_cors`

## 四、内置用户

| 用户名 | 密码  | 权限       | 备注                                                         |
| ------ | ----- | ---------- | ------------------------------------------------------------ |
| admin  | admin | 管理员用户 | 负责上传视频至版权库(版权库的初始视频，均由该用户上传)，可以进行版权库管理 |
| r      | 12345 | 普通用户   | 上传一些测试用例                                             |

## 五、如何运行

**<u>运行前请更改config.py中的配置常量！！！！！！！</u>**

用`pycharm`打开该工程
在**根目录**下运行`run.py`
打开 http://127.0.0.1:5000/即可访问