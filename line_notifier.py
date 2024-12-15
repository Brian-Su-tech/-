import requests
from config import LINE_NOTIFY_TOKEN
from utils import get_web_url

class LineNotifier:
    def __init__(self):
        self.token = LINE_NOTIFY_TOKEN
        self.api_url = "https://notify-api.line.me/api/notify"
        
    def send_startup_message(self):
        """發送系統啟動訊息，包含網頁介面 URL"""
        web_url = get_web_url()
        message = f"\n🖥️ 系統啟動\n🌐 網頁介面：{web_url}"
        self.send_message(message)
        
    def send_message(self, message):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        
        payload = {
            "message": message
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                data=payload
            )
            if response.status_code == 200:
                print("Line 通知發送成功")
            else:
                print(f"Line 通知發送失敗: {response.status_code}")
        except Exception as e:
            print(f"Line 通知發送錯誤: {str(e)}")