import contextlib
import csv
import datetime
import hashlib
import logging
import os
import sqlite3
import sys

import eel
import pandas as pd

with contextlib.redirect_stdout(None):
    # 🧜 Memo - terminalに出る "Hello from the pygame community." を消すため
    from pygame import mixer  # 📢

PATH_SOUND = os.path.join(sys.path[0], 'sound')

log_data = logging.getLogger(__name__)

class Handle(object):
    """
    カード情報の取り扱い

    Attributes
    ----------
    path : str
        homeディレクトリまでのパス
    display : None or str
        アプリケーションに表示するユーザー名等の文章
    path_db : str
        ユーザーのデータベースまでのPath
    path_csv : str
        記録のcsvファイルまでのPath
    path_sound : str
        アプリケーション音までのPath
    sound : bool
        音を鳴らすかどうか
    card : class
        カードのクラス
    sound_ok : class
        成功時のサウンド
    number : str
        学生証番号/教員・職員証番号
    idm : str
        カード固有のID番号
    user_hash : str
        idmをハッシュ関数に通した値
    user_name : str
        番号に紐付けられたユーザ名
    dt : list
        入退室時の時間

    Notes
    -----
        現在はidmをハッシュ関数に通していない。
    """

    def __init__(self, card, path, sound=True):
        """
        Parameters
        ----------
        card : class
            カードのクラス
        path : str
            homeディレクトリまでのパス
        sound : bool, default True
            アプリケーションの音を出す(Ture)か出さない(False)か
        """
        self.path = path
        path_db = os.path.join(path, 'data', 'list.db')
        path_log = os.path.join(path, 'data', 'log.csv')
        self.display = None
        self.path_db, self.path_csv, self.path_sound = path_db, path_log, PATH_SOUND
        self.sound, self.card = sound, card

        if self.sound:
            mixer.init()
            self.sound_ok = mixer.Sound(os.path.join(self.path_sound, 'mc.wav'))  # 📢
            self.sound_ok.set_volume(1)


    def __call__(self):
        """
        propertyとしてのアクセス用

        Returns
        -------
        display : None or str
            アプリケーションに表示するユーザー名等の文章
        """
        if self.card.info:

            self.number, self.idm = self.card.info
            self._get_hash()
            self._get_user_name()
            self._make_log()
            self._write_csv()
            self._make_display()
        return self.display

    def _get_hash(self):
        """
        ハッシュ関数に通す
        """
        self.user_hash = make_hash(self.idm, self.number)

    def _get_user_name(self):
        """
        idmを元にUser名を検索する
        """
        with sqlite3.connect(self.path_db) as conn:
            cur = conn.cursor()
            cur.execute("select * from miyano where device1=?",(self.user_hash,))
            data = cur.fetchall()
            cur.close()
        self.user_name = data[0][1] if data else None

    def _make_log(self):
        """
        入退室時の時刻を整える
        """
        self.dt = [datetime.datetime.now(), self.number, True]

    def _write_csv(self,add=None):
        """
        入退室時の記録(書き込み)
        """
        if self.user_name:
            with open(self.path_csv, 'a', newline="", encoding='utf_8_sig') as f:
                writer = csv.writer(f, delimiter=",")
                if add is not None:
                    self.dt[2]=add
                writer.writerow(self.dt)

    def _make_display(self):
        """
        表示を整える
        """
        if self.user_name:
            if self.sound:
                self.sound_ok.play()  # 📢

            hour = datetime.datetime.now().hour
            if (today(self.path) == self.number).sum()%2==0:
                greeting = 'お疲れさまでした'
            elif hour < 10:
                greeting = 'おはようございます'
            elif hour <15:
                greeting = 'こんにちは'
            else:
                greeting = 'こんばんは'
            self.display = f'{greeting} {self.user_name} さん'
        else:
            self.display = 'このカードは登録されていません。'

    def __repr__(self):
        return 'Handle a Card'

class EasyHandle(Handle):
    """
    カードを使用しない場合の取り扱い
    """
    def __init__(self, number, name, path):
        super().__init__(None, path)
        self.user_name, self.number = name, number
        self._make_log()
        self._write_csv(False)
        self._make_display()

# ---

def make_hash(idm, number):
    """
    ハッシュ値を作る。

    Parameters
    ----------
    idm : str
        カード固有のID番号
    number : str
        学生証番号/教員・職員証番号

    Returns
    -------
    h : str
        idmのハッシュ値

    Notes
    -----
        現在は完全にスルーしています。
    """
    h = idm  # + number + LAB
    return h  # hashlib.sha256(h.encode()).hexdigest()

# ---

def today(path):
    """
    本日分の入退室記録を回収

    Parameters
    ----------
    path : str
        homeディレクトリまでのパス

    Returns
    -------
    dts : list
        本日分のデータ
    """
    path_log = os.path.join(path, 'data', 'log.csv')
    df = pd.read_csv(path_log,header=None, names=['date','number','card'])
    df['date']=pd.to_datetime(df['date'])

    td = datetime.datetime.now().replace(hour=0, minute=0, second=0,microsecond=0)
    #tm = td+datetime.timedelta(days=1)
    df = df[(td <= df['date'])]

    return df['number']

def room(path):
    """
    現在の在室者のリストアップ

    Parameters
    ----------
    path : str
        homeディレクトリまでのパス

    Returns
    -------
    in_room : list
        現在の在室者のリスト
    """
    name_list = get_users_name(path)

    df = today(path)
    f = lambda x: x%2!=0

    df = df.value_counts()

    in_room = []
    for number in df[df.apply(f)].index.to_list():
        try:
            in_room.append(name_list[str(number)])
        except KeyError:
            pass
    return in_room

def get_users_name(path):
    """
    登録されているユーザ情報の回収

    Parameters
    ----------
    path : str
        homeディレクトリまでのパス

    Returns
    -------
    name_dict : dict
        登録ユーザ情報の辞書
    """
    path_db = os.path.join(path, 'data', 'list.db')
    name_list = []
    with sqlite3.connect(path_db) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('select * from miyano')
        for row in cur:
            d = (row['number'], row['name'])
            name_list.append(d)
        cur.close()
    name_dict = dict(name_list)
    return name_dict

def register_user(name, device1, number, path):
    """
    ユーザ情報の登録

    Parameters
    ----------
    name : str
        ユーザ名
    device1 : str
        idm
    number : str
        学生証番号/教員・職員証番号
    path : str
        homeディレクトリまでのパス

    Returns
    -------
    success : bool
        登録に成功(true)したか失敗(false)したか
    """
    path_db = os.path.join(path, 'data', 'list.db')
    if "" in [name, device1, number]:
        return False
    with sqlite3.connect(path_db) as conn:
        cur = conn.cursor()
        cur.execute('select max(id) from miyano')
        _id = cur.fetchall()[0][0] or 0  # 初期登録時は0でいいのか問題は顕在。この処理で不適合ある？

        try:
            cur.execute('insert into miyano (id, name, device1, number) values(?, ?, ?, ?)', (_id+1, name, device1, number))
            conn.commit()
            success = True
        except sqlite3.IntegrityError as e:
            success = False
        cur.close()
    return success

def delete_user(number, path):
    """
    ユーザ情報の消去

    Parameters
    ----------
    number : str
        学生証番号/教員・職員証番号
    path : str
        homeディレクトリまでのパス

    Returns
    -------
    success : bool
        削除に成功(true)したか失敗(false)したか
    """
    path_db = os.path.join(path, 'data', 'list.db')
    with sqlite3.connect(path_db) as conn:
        cur = conn.cursor()
        cur.execute('select * from miyano')
        before_datas = cur.fetchall()
        cur.execute('delete from miyano where number=?',(number,))
        cur.execute('select * from miyano')
        after_datas = cur.fetchall()
        cur.close()
        conn.commit()
    success = False if before_datas == after_datas else True
    return success

if __name__ == "__main__":
    path = os.path.join(sys.argv[1],'.deiri')