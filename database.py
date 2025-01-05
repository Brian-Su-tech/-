import mysql.connector
from datetime import datetime

class Database:
    def __init__(self):
        self.config = {
            'user': 'face_user',
            'password': 'user',
            'host': 'localhost',
            'database': 'face_rec'
        }
    
    def connect(self):
        return mysql.connector.connect(**self.config)
    
    def add_recognition_log(self, person_name):
        conn = self.connect()
        cursor = conn.cursor()
        
        sql = "INSERT INTO recognition_logs (person_name) VALUES (%s)"
        cursor.execute(sql, (person_name,))
        
        conn.commit()
        cursor.close()
        conn.close()