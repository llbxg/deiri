import logging
import os
import signal
import sys
import threading
import time

import eel

from src.app import App
from src.card import Card
from src.data import delete_user, EasyHandle, get_users_name, register_user, room
from src.startup import start_up

from src.reservation import resd, tdd, getdated, delscheduled

# init
PATH_USER_DATA = start_up(sys.argv)


# for log
formatter = '%(levelname)s : %(asctime)s : %(name)s : %(message)s'
logging.basicConfig(filename=f'{PATH_USER_DATA}/log/err.log',level=logging.WARN, format=formatter)

from nfc.clf import log
log.setLevel(logging.WARN)

from src.app import log_app
log_app.setLevel(logging.INFO)


@eel.expose
def count_checkbox(n):
    count_click(n)

# for main - 在室状況の確認
@eel.expose
def room_members():
    return room(PATH_USER_DATA)

# for reg - 登録したいカードの読み込み用
@eel.expose
def reading():
    c = Card(timeout_sec=0.1)
    #print(c.number.strip())
    return [n, c.idm] if (n := c.number) is not None else None

# for reg - dbにUser情報を登録
@eel.expose
def reg(idm, number, name):
    #print(idm.strip(), number.strip(), name)
    return register_user(name, idm.strip(), number.strip(), PATH_USER_DATA)

# for del - 登録しているUser情報を削除
@eel.expose
def delete(number):
    return delete_user(number, PATH_USER_DATA)

# for del & manual - User情報の取得
@eel.expose
def check_all_users():
    return get_users_name(PATH_USER_DATA)

# for manual - Userの出入
@eel.expose
def instant_deiri(name, number):
    display = EasyHandle(number, name, PATH_USER_DATA).display
    #print(display)
    eel.say_hello_or_seeu2("(No card)"+display)

# App内で共有したい変数があるので、初動でクラスを定義
app = App(PATH_USER_DATA)

@eel.expose
def where_am_i(where):
    app.where_am_i(where)

def page_transition(page, sockets):
    # Eelのcall_backは基本的にページ遷移時に起動する
    app.im_here = None

@eel.expose
def connectDevice():
    return app.device

@eel.expose
def system_exit():
    sys.exit()

def run():
    try:
        eel.init(sys.path[0]+'/web')
        eel.start(
            'html/contents/load.html',
            jinja_templates="html",
            close_callback=page_transition,
            mode=None,
            port=8080,
        )
    except Exception as e:
        #print(e)
        pass


if __name__ == "__main__":
    # Res
    @eel.expose
    def res(start, finish, number):
        resd(PATH_USER_DATA, start, finish, number)

    @eel.expose
    def timedate():
        return tdd(PATH_USER_DATA)

    @eel.expose
    def getdate(y, m, d):
        return getdated(PATH_USER_DATA, y, m, d)

    @eel.expose
    def delschedule(a):
        return delscheduled(PATH_USER_DATA, a)


    run()