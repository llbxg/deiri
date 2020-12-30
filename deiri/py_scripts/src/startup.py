import os
import sqlite3

def start_up(args):
    path = os.path.join(args[1],'.deiri')

    if not (os.path.exists(path_data:=os.path.join(path, 'data'))):
        os.makedirs(path_data, exist_ok=True)

    if not (os.path.exists(dbname :=os.path.join(path_data, 'list.db'))):
        # ここで異常でも出したほうが良いかな？？
        with sqlite3.connect(dbname) as conn:
            cur = conn.cursor()
            cur.execute('CREATE TABLE "miyano" ( "id" INTEGER NOT NULL UNIQUE, "name" TEXT NOT NULL, "device1" TEXT NOT NULL UNIQUE, "number" TEXT UNIQUE, PRIMARY KEY("id") )')
            conn.commit()

    if not (os.path.exists(csvname :=os.path.join(path_data, 'log.csv'))):
        with open(csvname, mode='w') as f:
            f.write('')

    if not (os.path.exists(csvname :=os.path.join(os.environ.get('DEIRI_AD_TEMP'), 'ad.csv'))):
        with open(csvname, mode='w') as f:
            f.write('')

    if not (os.path.exists(path_log:=os.path.join(path, 'log'))):
        os.makedirs(path_log, exist_ok=True)

    if not (os.path.exists(csvname :=os.path.join(path_log, 'log_from_mc.csv'))):
        with open(csvname, mode='w') as f:
            f.write('')

    if not (os.path.exists(errlog :=os.path.join(path_log, 'err.log'))):
        with open(errlog, mode='w') as f:
            f.write('')


    return path