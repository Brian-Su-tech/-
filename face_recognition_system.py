import RPi.GPIO as GPIO
import time
from led_controller import LEDController
from camera_processor import CameraProcessor
from config import BTN_PIN, CHECK_INTERVAL, SIMILARITY_THRESHOLD
from line_notifier import LineNotifier
from database import Database

class FaceRecognitionSystem:
    def __init__(self):
        self.led = LEDController()
        self.camera = CameraProcessor()
        self.line_notifier = LineNotifier()
        self.is_processing = False
        self.last_check_time = time.time()
        self.check_interval = CHECK_INTERVAL
        
        GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # 發送系統啟動訊息
        self.line_notifier.send_startup_message()
        
        self.db = Database()
        
    def check_button(self):
        current_time = time.time()
        if current_time - self.last_check_time >= self.check_interval:
            self.last_check_time = current_time
            if GPIO.input(BTN_PIN) == GPIO.LOW and not self.is_processing:
                self.process_recognition()
    
    def process_recognition(self):
        self.is_processing = True
        self.led.turn_on_yellow()
        print("\n開始處理影像...")
        
        self.line_notifier.send_message("\n🔔 有人按下辨識按鈕！")
        
        self.camera.start_camera()
        person_name = self.camera.process_frame()
        
        # 記錄到資料庫
        self.db.add_recognition_log(person_name)
        
        print(f"\n辨識到: {person_name}")
        
        if person_name in ["Brian", "Candy"]:  # 如果是已知人物
            message = f"\n✅ 辨識通過\n👤 辨識到: {person_name}"
            self.line_notifier.send_message(message)
            print(f"辨識結果: {person_name} 通過 ✓")
            self.led.turn_off_yellow()
            self.led.turn_on_green()
        else:  # 如果是未知人物（???）
            message = "\n❌ 辨識失敗：未偵測到授權人員"
            self.line_notifier.send_message(message)
            print("\n辨識失敗：未偵測到授權人員")
            self.led.turn_off_yellow()
            self.led.turn_on_red()
            
        print("\n等待 10 秒...")
        time.sleep(10)
        
        self.led.turn_off_all()
        self.camera.stop_camera()
        self.is_processing = False
        print("處理完成\n")