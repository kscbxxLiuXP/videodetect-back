from flask import Blueprint, request
import json
from app.controller import MySqlUtil as DBUtil

FeedbackBlue = Blueprint("feedbackBlue", __name__)


@FeedbackBlue.route('/feedbackList')
def getFeedbackList():
    return DBUtil.getFeedbackList()


@FeedbackBlue.route('/newFeedback', methods=['POST'])
def newFeedback():
    data = json.loads(request.get_data(as_text=True))
    return DBUtil.newFeedback(data)


@FeedbackBlue.route('/replyFeedback', methods=['POST'])
def replyFeedback():
    data = json.loads(request.get_data(as_text=True))
    return DBUtil.replyFeedback(data)


@FeedbackBlue.route('/feebackSetReaded/<id>')
def feedbackSetReaded(id):
    return DBUtil.feedbackSetReaded(id)
