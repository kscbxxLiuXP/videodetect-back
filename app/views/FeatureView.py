from flask import Blueprint, request
import json
from app.controller import MySqlUtil as DBUtil

FeatureBlue = Blueprint("featureBlue", __name__)


@FeatureBlue.route('/getFeatureList')
def getFeatureList():
    return DBUtil.getFeatureList()
