#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/18 9:06 AM
# @Author  : Steven
# @Contact : 523348709@qq.com
# @Site    : 
# @File    : phone_sms.py
# @Software: PyCharm
import os
import sqlite3
import time
def get_database():
    os.system("adb shell su -c 'cp /data/data/com.android.providers.telephony/databases/mmssms.db /data/local/tmp'")
    os.system("adb shell su -c 'chmod 777 /data/local/tmp/mmssms.db' ")
    os.system("adb pull /data/local/tmp/mmssms.db ./")

def insert_sms(address,date,body='This is test Text'):
    address=str(address)
    date=str(date)
    body=str(body)

    conn=sqlite3.connect('./mmssms.db')
    cur=conn.cursor()
    sql1='insert into canonical_addresses VALUES (NULL,%s)'%address
    cur.execute(sql1)

    recipient_ids=str(cur.lastrowid)
    sql2='insert into threads(_id,date,message_count,recipient_ids,snippet,type) VALUES(NUll,%s,0,%s,%s,1)'%(date,recipient_ids,address)
    cur.execute(sql2)

    thread_id=str(cur.lastrowid)
    sql3='insert into sms(_id,thread_id,address,date,date_sent,type,body) VALUES(NULL,%s,%s,%s,%s,1,\'%s\')'%(thread_id,address,date,date,body)
    cur.execute(sql3)

    cur.close()
    conn.commit()
    conn.close()

def push_database():
    os.system('adb push ./mmssms.db /data/local/tmp/mmssms.db')
    os.system("adb shell su -c 'cp /data/local/tmp/mmssms.db /data/data/com.android.providers.telephony/databases/mmssms.db'")

if __name__ == '__main__':

    address='100086'
    body='hello,这里是10086'
    date=time.time()
    get_database()
    insert_sms(address=address,date=date,body=body)
    push_database()
