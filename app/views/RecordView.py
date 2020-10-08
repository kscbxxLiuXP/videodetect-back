from flask import Blueprint, request
import json
from app.controller import MySqlUtil as DBUtil

RecordBlue = Blueprint("recordBlue", __name__)


@RecordBlue.route('/getUploadRecord/<username>')
def getUploadRecord(username):
    return DBUtil.getUploadRecord(username)


@RecordBlue.route('/getContentList/<username>')
def getContentList(username):
    return DBUtil.getContentList(username)


@RecordBlue.route('/getVideoList')
def getVideoList():
    return DBUtil.getVideoList()
