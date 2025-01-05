import RPi.GPIO as GPIO
from face_recognition_system import FaceRecognitionSystem
import time
from flask import Flask, render_template, request
from threading import Thread
from config import FLASK_HOST, FLASK_PORT
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# 資料庫連線函數
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="face_rec"
    )

@app.route('/')
def index():
    # 查詢今天的日期
    today_date = datetime.now().strftime('%Y-%m-%d')

    # 建立資料庫連線
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 查詢今天的來訪人數
    cursor.execute("SELECT COUNT(id) AS visitor_count FROM recognition_logs WHERE DATE(timestamp) = %s", (today_date,))
    visitor_count = cursor.fetchone()["visitor_count"]

    # 查詢所有姓名及對應的訪問時間
    cursor.execute("SELECT person_name, timestamp FROM recognition_logs")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # 整理資料供前端使用
    data = {}
    for row in rows:
        name = row['person_name']
        time = row['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        if name not in data:
            data[name] = []
        data[name].append(time)

    return render_template('index.html', data=data, visitor_count=visitor_count)


@app.route('/search', methods=['POST'])
def search():
    # 接收表單數據
    name = request.form.get('name')  # 取得 'name' 的值
    time = request.form.get('time')  # 取得 'time' 的值

     # 確保時間格式匹配存放的文件名格式
    formatted_time = time.replace(" ", "_").replace(":", "").replace("-","")

    return render_template('search.html', name=name, time=formatted_time)


def run_flask():
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=False)

def init_gpio():
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)

def main():
    try:
        init_gpio()
        
        # 在背景執行 Flask 伺服器
        flask_thread = Thread(target=run_flask)
        flask_thread.daemon = True
        flask_thread.start()
        
        system = FaceRecognitionSystem()
        print("系統已啟動，請按下按鈕開始辨識...")
        
        while True:
            system.check_button()
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n程式結束")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()