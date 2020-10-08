import MySQLdb

import config


def newConnection():
    new_db = MySQLdb.connect(
        "localhost",
        config.SQL_USERNAME,
        config.SQL_PSD,
        "videodetect",
        charset='utf8'
    )
    return new_db
