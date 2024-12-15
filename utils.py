import socket
from config import FLASK_PORT

def get_web_url():
    # 獲取實際的 IP 位址（不使用 hostname）
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 不需要實際連接
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return f"http://{ip_address}:{FLASK_PORT}"