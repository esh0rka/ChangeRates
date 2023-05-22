from pyoxr import OXRClient
import sqlite3
import boto3
import sys


conn = sqlite3.connect('current_exchange_rate.db')
cursor = conn.cursor()
cursor.execute('DROP TABLE current_exchange_rate')
cursor.execute('''CREATE TABLE IF NOT EXISTS current_exchange_rate
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   currency TEXT NOT NULL,
                   rate INTEGER)''')

oxr_cli = OXRClient(app_id=sys.argv[1])
result = oxr_cli.get_latest()

for currency, rate in result['rates'].items():
    cursor.execute("INSERT INTO current_exchange_rate (currency, rate) VALUES (?, ?)", (currency, rate))

conn.commit()
conn.close()

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

s3.upload_file('current_exchange_rate.db', 'change-rates', 'current_exchange_rate.db')
