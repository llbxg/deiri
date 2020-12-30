import contextlib
import datetime
import logging
import os
import signal
import sys
import threading
import time

import eel

from .card import Card
from .data import Handle

log_app = logging.getLogger(__name__)

class App(object):
    """
    アプリケーションのメイン
    メインページでは常に読み込みループを回す。それ以外では、任意のタイミングのみ起動。

    Attributes
    ----------
    path : str
        homeディレクトリまでのパス
    im_here : str
        現在いるページ情報
    device : bool
        デバイスに接続されている(true)かされていない(false)か
    event : bool
        Cardの読み込み状態。可能ならtreu
    alive : bool
        main-loopの存命条件
    thread_main : class
        メインのループスレッド
    """

    def __init__(self, path):
        """
        初期値設定と、カードリーダーの接続確認。

        Parameters
        ----------
        path : str
            homeディレクトリまでのパス
        """
        self.path = path
        self.im_here = "main"

        self.device = False

        # Setup Threading Start
        self.event = True  # 🚩
        self.alive = True

        # 初回起動時のデバイスの接続確認
        if Card(timeout_sec=0).access:
            self.thread_main = threading.Thread(target=self.__main_loop).start()
            self.device = True

    def __main_loop(self):
        """
        メインのループ

        Notes
        -----
        ループの抜け出し方が非常にダサい。
        Eelの終了が行えない😇 Eelのcall_backがページ遷移に対応するため。
        端的に悲しいけど、とりあえずこのthread内で強制終了`os.kill(os.getpid(), signal.SIGINT)`
        """
        log_app.info('Thread(Main Loop) Start')
        while self.alive:
            if self.im_here is None:
                eel.sleep(1)  # 💣💥 以下の処理はダサい。
                if self.im_here is None:
                    self.alive= False

            elif self.event:  # 🚩
                started = time.time()
                card = Card()

                if not card.access:
                    eel.noDevice()
                    eel.sleep(5)
                    break

                display = Handle(card, self.path)()

                if display:
                    eel.say_hello_or_seeu(display)
                    eel.sleep(4)

                if ((remaining := 4 -(time.time() - started))) > 0:
                    eel.sleep(remaining)

            else:
                eel.sleep(4)

        log_app.info('Thread(Main Loop) Finish')
        os.kill(os.getpid(), signal.SIGINT)

    def where_am_i(self, where):
        self.im_here = where
        self.event = (self.im_here == 'main') or False  # 🚩