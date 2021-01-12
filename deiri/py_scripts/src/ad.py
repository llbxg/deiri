import csv
import datetime
import os

# ad でのクリック数カウンター
def count_click(n):
    path = os.path.join(os.environ.get('DEIRI_AD_TEMP'), 'ad.csv')
    with open(path, 'a', newline="", encoding='utf_8_sig') as f:
        dt_now = datetime.datetime.now()
        writer = csv.writer(f, delimiter=",")
        writer.writerow([dt_now, n])