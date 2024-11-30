# Install WriteCloud Service

import sqlite3
import logging
import os
import time

if os.path.exists('install.lock'):
    exit('检测到install.lock文件,服务可能已安装')

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
ip = s.getsockname()[0]

serverName = input('输入服务器名称: ')
userName = input('输入用户名: ')
userPassword = input('输入用户密码: ')

if not serverName or not userName or not userPassword:
    exit('某一项没有数据,请重新执行脚本并填写')
os.makedirs('data')
f = open('data/main.db', 'w')
f.close()
conn = sqlite3.connect('data/main.db')
c = conn.cursor()
c.execute('''CREATE TABLE MAIN
    (ID INT PRIMARY KEY     NOT NULL,
    ServerName         TEXT,
    UserName           TEXT,
    UserPassword       TEXT,
    JoinTime           INT,
    LastLogin           INT,
    LastLoginIP       TEXT,
    NovelID           TEXT,
    AllText        INT);''')
c.execute('INSERT INTO MAIN (ID,ServerName,UserName,UserPassword,JoinTime,LastLogin,LastLoginIP,NovelID,AllText) \
    VALUES (?,?,?,?,?,?,?,?,?)',(1, serverName, userName, userPassword, int(time.time()), int(time.time()), ip, '', 0))
conn.commit()
conn.close()
print('主数据库创建成功')
os.makedirs('data/novel')
print('生成小说文件夹成功')
os.makedirs('data/synceditor')
print('生成同步书写文件夹成功')
import yaml
data = {'allow_remote_login':False,'allow_sync_editor':True,'synce_ws_port':'63300','max_login_devices':'3','device_timeup':'864000000','max_password_wrong':'3'}
with open('data/settings.yml', 'w', encoding='utf-8') as f:
    yaml.dump(data=data, stream=f, allow_unicode=True)
print('生成设置文件完成')
f.close()
f = open('install.lock', 'w')
f.close()
print('安装已完成,欢迎使用 WriteCloud\n部分设置已使用默认值,您可在设置页面进行调整')