import cv2
import numpy as np
import time
import os
from datetime import datetime
from config import CAPTURE_TIME, TARGET_FRAMES, DISPLAY_INTERVAL

class CameraProcessor:
    def __init__(self):
        self.cap = None
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('face.yml')
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        self.labels = ['???', 'Brian', 'Candy']
        
        # 建立主資料夾
        self.base_folder = 'captured_photos'
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)
            
        # 建立各人物的子資料夾
        self.person_folders = {
            'Brian': os.path.join(self.base_folder, 'brian'),
            'Candy': os.path.join(self.base_folder, 'candy'),
            '???': os.path.join(self.base_folder, 'unknown')
        }
        
        # 確保所有子資料夾都存在
        for folder in self.person_folders.values():
            if not os.path.exists(folder):
                os.makedirs(folder)
                
    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
    def stop_camera(self):
        if self.cap:
            self.cap.release()
            
    def process_frame(self):
        results = []
        frame_count = 0
        check_interval = 0.5
        
        # 記錄最佳影像（不論是否偵測到人臉）
        best_image = None
        best_face_image = None
        best_similarity = 0
        best_person_idx = 0  # 預設為未知人物（索引0）
        
        print("\n開始擷取影像...")
        start_time = time.time()
        last_check_time = start_time
        
        while frame_count < TARGET_FRAMES and (time.time() - start_time) <= CAPTURE_TIME:
            ret, frame = self.cap.read()
            if not ret:
                continue
                
            current_time = time.time()
            if current_time - last_check_time >= check_interval:
                frame = cv2.resize(frame, (540, 300))
                # 保存第一張影像作為備用
                if best_image is None:
                    best_image = frame.copy()
                    
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray)
                
                if len(faces) > 0:  # 如果偵測到人臉
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                        
                        id_num, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                        similarity = (100 - min(confidence, 100)) / 100
                        
                        if confidence < 60:
                            name_idx = id_num
                        else:
                            name_idx = 0
                            
                        results.append((name_idx, similarity))
                        
                        # 如果這是最佳的人臉影像，就保存下來
                        if similarity > best_similarity:
                            best_similarity = similarity
                            best_person_idx = name_idx
                            best_face_image = frame.copy()
                        
                        text = self.labels[name_idx]
                        cv2.putText(frame, f"{text}", (x,y-5),
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
                
                frame_count += 1
                last_check_time = current_time
                
                if frame_count % DISPLAY_INTERVAL == 0:
                    elapsed_time = current_time - start_time
                    print(f"已擷取 {frame_count} 張影像，已用時間: {elapsed_time:.1f} 秒")
            
            cv2.imshow('Frame', frame)
            cv2.waitKey(1)
        
        cv2.destroyAllWindows()
        
        # 決定最終的辨識結果和儲存位置
        if results:
            person_stats = {}
            for idx, similarity in results:
                if idx not in person_stats:
                    person_stats[idx] = []
                person_stats[idx].append(similarity)
            
            best_person = max(person_stats.items(), 
                            key=lambda x: (len(x[1]), sum(x[1])/len(x[1])))
            
            final_person_idx = best_person[0]
            final_person_name = self.labels[final_person_idx]
        else:
            final_person_name = "???"
        
        # 儲存影像
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_image = best_face_image if best_face_image is not None else best_image
        
        # 根據最終辨識結果選擇儲存資料夾
        save_folder = self.person_folders[final_person_name]
        filename = f"{timestamp}.jpg"
        filepath = os.path.join(save_folder, filename)
        cv2.imwrite(filepath, save_image)
        print(f"已儲存影像到 {final_person_name} 資料夾：{filename}")
        
        return final_person_name