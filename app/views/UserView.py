from flask import Blueprint, request, make_response, jsonify
import json
from app.controller import MySqlUtil as DBUtil
from app.controller.Utils import responseGen

UserBlue = Blueprint("userBlue", __name__)


# 检测用户名是否存在
@UserBlue.route('/checkUser/<username>')
def checkUser(username):
    tmp = DBUtil.checkUser(username)
    re = {'code': tmp}
    return json.dumps(re)


# 检测用户密码是否正确
@UserBlue.route('/checkPassword/<username>/<password>')
def checkPassword(username, password):
    re = DBUtil.checkPassword(username, password)
    return json.dumps(re)


@UserBlue.route('/getTest', methods=['GET'])
def getMethodTest():
    return 0


@UserBlue.route('/postTest', methods=['POST'])
def postMethodTest():
    form = json.loads(request.get_data(as_text=True))
    print(form)
    print(form.get('username'))
    res = responseGen(0, 'success', '')
    return res


# 注册用户
@UserBlue.route('/registerUser', methods=['POST'])
def registerUser():
    data = request.get_data(as_text=True)
    re = DBUtil.registerUser(data)
    return re


# 获取用户list
@UserBlue.route('/getUserList')
def getUserList():
    return DBUtil.getUserList()


# 获取用户主页信息
@UserBlue.route('/dashboard/<username>')
def getUserDashboard(username):
    return DBUtil.getUserDashboard(username)


# 获取用户信息
@UserBlue.route('/getUser/<username>')
def getUser(username):
    return DBUtil.getUser(username)


# 更新用户信息（不含头像）
@UserBlue.route('/updateUser/<username>', methods=['POST'])
def updateUser(username):
    data = request.get_data(as_text=True)
    return DBUtil.updateUser(username, data)


# 发邮件时检索用户
@UserBlue.route('/fetch/<keyword>')
def fetchUser(keyword):
    return DBUtil.fetchUser(keyword)


# 删除用户
@UserBlue.route('/deleteUser/<username>')
def deleteUser(username):
    return DBUtil.deleteUser(username)


@UserBlue.route('/resetPassword/<username>')
def resetPassword(username):
    return DBUtil.resetPassword(username)

#管理员更改用户密码
@UserBlue.route('/changePassword', methods=['POST'])
def changePassword():
    data = request.get_data(as_text=True)
    return DBUtil.changePassword(json.loads(data))



@UserBlue.route('setAuth', methods=['POST'])
def setAuth():
    data = request.get_data(as_text=True)
    return DBUtil.setAuth(json.loads(data))
