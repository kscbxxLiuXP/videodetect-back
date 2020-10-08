from flask import Blueprint, request
import json
from app.controller import MySqlUtil as DBUtil

AppealBlue = Blueprint("appealBlue", __name__)


@AppealBlue.route('/getFailedVideoList/<username>')
def getFailedVideoList(username):
    return DBUtil.getFailedVideoList(username)


@AppealBlue.route('/addNewAppeal/<username>', methods=['POST'])
def addNewAppeal(username):
    data = json.loads(request.get_data(as_text=True))
    return DBUtil.addNewAppeal(data, username)


@AppealBlue.route('/getAppealList/<username>/<type>')
def getAppealList(username, type):
    return DBUtil.getAppealList(username, int(type), all=False)


@AppealBlue.route('/getAppealListAll/<type>')
def getAllAppealList(type):
    return DBUtil.getAppealList('', int(type), all=True)


@AppealBlue.route('/getAppealCount/<username>')
def getAppealCount(username):
    return DBUtil.getAppealCount(username, all=False)


@AppealBlue.route('/getAllAppealCount')
def getAllAppealCount():
    return DBUtil.getAppealCount('', all=True)


@AppealBlue.route('/getAppealDetail/<id>')
def getAppealDetail(id):
    return DBUtil.getAppealDetail(id)


@AppealBlue.route('/resolveAppeal', methods=['POST'])
def resolveAppeal():
    data = json.loads(request.get_data(as_text=True))
    return DBUtil.resolveAppeal(data)
