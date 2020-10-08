from flask import Blueprint, request
import json
from app.controller import MySqlUtil as DBUtil

MessageBlue = Blueprint("messageBlue", __name__)


@MessageBlue.route('/sendMessage', methods=['POST'])
def sendMessage():
    msgData = request.get_data(as_text=True)
    return DBUtil.sendMessage(msgData)


@MessageBlue.route('/getMessageList/<username>', methods=['GET'])
def getMessageList(username):
    return DBUtil.getMessageList(username)


@MessageBlue.route('/setMessageState', methods=['POST'])
def setMessageState():
    data = json.loads(request.get_data(as_text=True))
    return DBUtil.setMessageState(data)


@MessageBlue.route('/getUnreadCount/<username>', methods=['GET'])
def getUnreadCount(username):
    return DBUtil.getUnreadCount(username)


@MessageBlue.route('/deleteMessage/<id>', methods=['GET'])
def deleteMessgae(id):
    return DBUtil.deleteMessage(int(id))
