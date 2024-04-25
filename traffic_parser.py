import xml.etree.ElementTree as ET
import sqlite3


tree = ET.parse('GetVD.xml')
root = tree.getroot()
exchange_time = root[1].text
section_dataset = root[-1]
traffic_data = []
for data in section_dataset:
    section_id = data[0].text
    name = ''
    text = data[1].text.split(' ')
    for t in text:
        t = t.replace('　', ' ')
        if len(t.strip()) > 0:
            name += t.strip() + ' '
    avg_speed = data[2].text
    avg_occ = data[3].text
    total_vol = data[4].text
    traffic_data.append((exchange_time, section_id, name, float(avg_speed), float(avg_occ), float(total_vol)))

con = sqlite3.connect("traffic.db")
cur = con.cursor()

cur.executemany("REPLACE INTO data VALUES(?, ?, ?, ?, ?, ?)", traffic_data)
con.commit()
con.close()
