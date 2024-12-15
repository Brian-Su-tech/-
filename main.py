import RPi.GPIO as GPIO
from face_recognition_system import FaceRecognitionSystem
import time
from flask import Flask
from threading import Thread
from config import FLASK_HOST, FLASK_PORT

app = Flask(__name__)

@app.route('/')
def home():
    return "人臉辨識系統網頁介面"

def run_flask():
    app.run(host=FLASK_HOST, port=FLASK_PORT)

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