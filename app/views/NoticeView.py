from flask import Blueprint, request
import json
from app.controller import MySqlUtil as DBUtil

NoticeBlue = Blueprint("noticeBlue", __name__)


@NoticeBlue.route('/noticeList')
def getNoticeList():
    return DBUtil.getNoticeList()


