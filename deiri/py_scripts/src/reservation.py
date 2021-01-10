import csv
import datetime
import logging
import os
import time

import eel
import pandas as pd

from .data import get_users_name

def resd(path, start, finish, number):
    path_res = os.path.join(path, 'data', 'res.csv')
    s = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M')
    f = datetime.datetime.strptime(finish, '%Y-%m-%d %H:%M')
    if not s>=f:
        df = pd.read_csv(path_res,header=None, names=['start','finish','number'])
        df['start']=pd.to_datetime(df['start'])
        df['finish']=pd.to_datetime(df['finish'])

        ans1 = df[~((s < df['start']) & (f <= df['start']))]
        ans2 = df[~((s >= df['finish']) & (f > df['finish']))]

        if (len(ans1)==0 or len(ans2) == 0):
            #df.append()
            #df.to_csv(path_res,header=False, index=False)
            with open(path_res, 'a', newline="", encoding='utf_8_sig') as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow([start, finish, number])

            eel.nok(f'予約できました。')
            eel.clean()

        else:
            eel.nok(f'予約できませんでした')
    else:
        eel.nok('予約できませんでした。')

def tdd(path):
    path_res = os.path.join(path, 'data', 'res.csv')
    df = pd.read_csv(path_res,header=None, names=['start','finish','number'])
    df['start']=pd.to_datetime(df['start'])
    df['finish']=pd.to_datetime(df['finish'])
    df = df[df['start']>=datetime.datetime.now()]
    f = lambda x: f"{x[0].strftime('%m/%d %H時')} ~ {x[1].strftime('%m/%d %H時')} {x[2]}"
    new_df_1 = df.apply(f, axis=1)

    return new_df_1.to_list() if len(new_df_1)!=0 else []

def getdated(path, y, m, d):
    d_0 = datetime.datetime(y, m, d)
    d_1 = d_0 + datetime.timedelta(days=1)

    path_res = os.path.join(path, 'data', 'res.csv')
    df = pd.read_csv(path_res,header=None, names=['start','finish','number'])
    df['start']=pd.to_datetime(df['start'])
    df['finish']=pd.to_datetime(df['finish'])

    df = df[((d_0 <= df['start']) & (d_1 > df['start'])) | ((d_0 <= df['finish']) & (d_1 > df['finish']))]
    df=df.sort_values(by="start")

    user_list=get_users_name(path)
    f = lambda x: [x[0].strftime('%Y,%m,%d, %H,%M').split(','), x[1].strftime('%Y,%m,%d, %H,%M').split(','), user_list[str(x[2])]]#f"{x[0)].strftime('%d %H時')} ~ {x[1].strftime('%d %H時')} {x[2]}"
    new_df_1 = df.apply(f, axis=1)

    return new_df_1.to_list() if len(new_df_1)!=0 else []

def delscheduled(path, a):
    y, mo, d, h, m = [int(x) for x in a.split(',')]
    d_0 = datetime.datetime(y, mo, d, h, m)

    path_res = os.path.join(path, 'data', 'res.csv')
    df = pd.read_csv(path_res,header=None, names=['start','finish','number'])
    df['start']=pd.to_datetime(df['start'])
    df['finish']=pd.to_datetime(df['finish'])

    df = df[d_0 !=df['start']]
    df.to_csv(path_res, header=False, index=False)

