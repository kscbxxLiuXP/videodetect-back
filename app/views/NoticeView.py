from flask import Blueprint, request
import json
from app.controller import MySqlUtil as DBUtil

NoticeBlue = Blueprint("noticeBlue", __name__)


@NoticeBlue.route('/noticeList')
def getNoticeList():
    return DBUtil.getNoticeList()


@NoticeBlue.route('/deleteNotice/<id>')
def deleteNotice(id):
    return DBUtil.deleteNotice(id)


@NoticeBlue.route('/newNotice', methods=['POST'])
def newNotice():
    data = json.loads(request.get_data(as_text=True))
    return DBUtil.newNotice(data)

@NoticeBlue.route('/updateNotice',methods=['POST'])
def updateNotice():
    data = json.loads(request.get_data(as_text=True))
    return DBUtil.updateNotice(data)