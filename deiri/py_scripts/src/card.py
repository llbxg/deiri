from binascii import hexlify
import time

import nfc
import usb1

class Card(object):
    """
    カード情報の取り扱い

    Attributes
    ----------
    timeout_sec : int
        カード情報へのアクセスのタイムアウト[s]
    number : str
        学生証番号/教員・職員証番号
    idm : str
        カード固有のID番号
    access : bool
        カードリーダーへの接続の成功(True)or失敗(False)の保存
    """

    def __init__(self, timeout_sec=4):
        """
        Parameters
        ----------
        timeout_sec : int, default 4
            カード情報へのアクセスのタイムアウト[s]
        """
        self.timeout_sec = timeout_sec
        self.number, self.idm = None, None
        self.access = False
        self.__connect_sp_error()

    def __connect_sp_error(self):
        """
        処理を行う

        Raises
        ------
        usb1.USBError
            デバイスの多重使用の確認
        IOError
            デバイスが接続されていないとき
        """
        try:
            self.__connect()
            self.access = True  # 🐝 timeoutでもaccessはTrueになるよ

        except usb1.USBError as e:
            # 'LIBUSB_ERROR_ACCESS': -3,
            # Access denied (insufficient permissions)
            #print(f"{e} -> Using one device at the same time")
            self.access = False

        except IOError as e:
            #print(f"{e} -> Unable to check device connection.")
            self.access = False

    def __connect(self):
        """
        カード読み取り時の各種設定とアクセスを行う。
        """
        with nfc.ContactlessFrontend('usb') as clf:
            rdwr_options = {
                'targets': ['212F' , '424F'],
                'on-connect': self.__on_connect,
                }

            # timeout処理
            after5s = lambda: time.time() - started > self.timeout_sec
            started = time.time()

            clf.connect(rdwr=rdwr_options, terminate=after5s)

    def __on_connect(self, tag):
        """
        対象とするカードから情報を取得する。
        Parameters
        ----------
        tag : class
            すべてのNFCタグ/カードの基本クラス

        Notes
        -----
            カードの種類によって番号の保存されている位置は異なる。
        """
        try:
            idm, pmm = tag.polling(system_code=0xfe00)
            tag.idm, tag.pmm, tag.sys = idm, pmm, 0xfe00

            sc = nfc.tag.tt3.ServiceCode(106, 0x0b)
            bc = nfc.tag.tt3.BlockCode(0, service=0)

            data = tag.read_without_encryption([sc], [bc])
            data = data.decode('utf-8').replace('\0', '')

            self.number = data[2:-2]
            self.idm = hexlify(idm).decode('utf-8')

        except nfc.tag.tt3.Type3TagCommandError:
            # 非対応カードはスルーするー。
            pass

    @property
    def info(self):
        """
        propertyとしてのアクセス用

        Returns
        -------
         : (str, str)
            番号と固有ID
        """
        return (self.number, self.idm) if (self.number and self.idm) else None

    def __repr__(self):
        return "I'm a card 😡"

if __name__ == "__main__":
    if Card(timeout_sec=0).access:
        print("ok")