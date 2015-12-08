from peewee import SqliteDatabase, TextField, IntegerField, Model, OperationalError
import os
import time


def gen_firefox_cookie(host, cookie):
    db = SqliteDatabase("{0}/cookies_hijacked/{1}.sqlite".format(os.path.abspath(os.path.join(os.getcwd(), os.pardir)),
                                                                 host))

    class moz_cookies(Model):
        baseDomain = TextField()
        appId = IntegerField(default=0)
        inBrowserElement = IntegerField(default=0)
        name = TextField()
        value = TextField()
        host = TextField()
        path = TextField()
        expiry = IntegerField()
        lastAccessed = IntegerField()
        creationTime = IntegerField()
        isSecure = IntegerField()
        isHttpOnly = IntegerField()

        class Meta:
            """
            indexes = (
                # create a unique
                (("name", "host", "path", "appId", "inBrowserElement"), True),
            )
            """
            database = db
    try:
        moz_cookies.create_table()
    except OperationalError:
        print "Database already exist, it will be updated"

    first_time_cokkie = time.time()
    expired_time_cookie = first_time_cokkie + 2592000

    for element in cookie.split(";"):
        cookie_name, cookie_value = element.split("=", 1)
        moz_cookies.create(
            baseDomain=host.replace("www.", ""),
            appId=0,
            inBrowserElement=0,
            name=cookie_name,
            value=cookie_value,
            host=".{0}".format(host.replace("www.", "")),
            path="/",
            expiry=expired_time_cookie,
            lastAccessed=first_time_cokkie,
            creationTime=first_time_cokkie,
            isSecure=0,
            isHttpOnly=0
        )
