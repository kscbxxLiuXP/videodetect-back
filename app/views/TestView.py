from flask import Blueprint
from app.models.TaskManager import taskManager

TestBlue = Blueprint("testBlue", __name__)


@TestBlue.route('/test')
def test1():
    return str(taskManager.number)


@TestBlue.route('/test/<id>')
def test(id):
    taskManager.addTask(id)
    return str(taskManager.number)
