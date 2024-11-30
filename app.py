# Install WriteCloud Service

from flask import Flask, render_template, request
import sqlite3
import logging
import random
import os
import time

app_port = 65300

if os.path.exists("app.log"):
    os.remove("app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
    filemode="a",
)

logging.info("WriteCloud安装程序已开始")
logging.info(f"WriteCloud Install 服务已在端口 {str(app_port)} 上启用")

authcode = random.randint(1111111111,9999999999)
print(f"验证码为: {authcode}")
print(f"WriteCloud Install 服务已在端口 {str(app_port)} 上启用,您可以访问 http://localhost:{app_port}/ 进入页面")

app = Flask(__name__)

@app.route('/')
def install():
    if os.path.exists("install.lock"):
        logging.error("检测到install.lock文件,服务可能已安装")
        return render_template('error.html', errorMessage="先前已安装过WriteCloud服务,若需再次安装,请按照文档指引删除文件")
    else:
        return render_template('install.html')

@app.route('/install_submit', methods=['POST'])
def install_submit():
    serverName = request.form.get('serverName')
    userName = request.form.get('userName')
    userPassword = request.form.get('userPassword')
    installAuth = request.form.get('installAuth')
    print(serverName)
    if installAuth != authcode:
        logging.error("安装验证码错误")
        return render_template('error.html', errorMessage="输入的验证码与控制台验证码不一致,请检查后重新输入")
    try:
        if not serverName or not userName or not userPassword:
            logging.error("缺少数据")
            return render_template('error.html', errorMessage=f"其中某一项没有数据")
        f = open('data/main.db', 'w')
        f.close()
        conn = sqlite3.connect('./data/main.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE MAIN
            (ID INT PRIMARY KEY     NOT NULL,
            ServerName         TEXT,
            UserName           TEXT,
            UserPassword       TEXT,
            JoinTime           INT,
            LastLogin           INT,
            NovelID           TEXT,
            AllText        INT);''')
        c.execute(f"INSERT INTO MAIN (ID,ServerName,UserName,UserPassword,JoinTime,LastLogin,NovelID,AllText) \
            VALUES (1,{serverName},{userName},{userPassword},{int(time.time())},{int(time.time())},'',0)")
        logging.info("主数据库创建成功")
        f = open("data/settings/settings.yml", "w")
        os.makedirs('data/novel')
        logging.info("生成小说文件夹成功")
        os.makedirs('data/synceditor')
        logging.info("生成同步书写文件夹成功")
        import yaml
        f = open("data/settings/settings.yml", "w")
        data = {'allow_remote_login':False,'allow_sync_editor':True,'synce_ws_port':'63300','max_login_devices':'3','device_timeup':'864000000','max_password_wrong':'3'}
        with open('data/settings/settings.yml', 'w', encoding='utf-8') as f:
            yaml.dump(data=data, stream=f, allow_unicode=True)
        print("生成设置文件完成")
        f.close()
        logging.info("安装已完成")
        return render_template('complete.html')
        
    except Exception as e:
        return render_template('error.html', errorMessage=f"Python发生错误:{e}")

if __name__ == '__main__':
    app.run(port=app_port)