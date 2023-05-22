from pyoxr import OXRClient
import sqlite3

conn = sqlite3.connect('current_exchange_rate.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS current_exchange_rate
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   currency TEXT NOT NULL,
                   rate INTEGER)''')

oxr_cli = OXRClient(app_id='6acee60892d849bfaa7d445181a112c1')
result = oxr_cli.get_latest()

for currency, rate in result['rates'].items():
    cursor.execute("INSERT INTO current_exchange_rate (currency, rate) VALUES (?, ?)", (currency, rate))

conn.commit()
conn.close()
