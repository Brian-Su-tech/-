import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
import time
from config import MODEL_PATH, LABELS_PATH, TARGET_FRAMES, CAPTURE_TIME, DISPLAY_INTERVAL

class CameraProcessor:
    def __init__(self, model_path=MODEL_PATH):
        self.cap = None
        self.interpreter = self.load_model(model_path)
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        # 載入標籤
        with open(LABELS_PATH, 'r') as f:
            self.labels = [line.strip().split()[1] for line in f.readlines()]
        
    def load_model(self, model_path):
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter
        
    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
    def stop_camera(self):
        if self.cap:
            self.cap.release()
            
    def preprocess(self, frame):
        resized = cv2.resize(frame, (224, 224))
        normalized = resized.astype(np.float32) / 255.0
        return np.expand_dims(normalized, axis=0)
            
    def process_frame(self):
        similarities = []
        frame_count = 0
        
        interval = CAPTURE_TIME / TARGET_FRAMES
        
        print("\n開始擷取影像...")
        start_time = time.time()
        last_capture_time = start_time
        
        while frame_count < TARGET_FRAMES and (time.time() - start_time) <= CAPTURE_TIME:
            ret, frame = self.cap.read()
            if not ret:
                continue
                
            current_time = time.time()
            if current_time - last_capture_time >= interval:
                processed_data = self.preprocess(frame)
                similarity = self.calculate_similarity(processed_data)
                if similarity is not None:
                    similarities.append(similarity)
                frame_count += 1
                last_capture_time = current_time
                
                if frame_count % DISPLAY_INTERVAL == 0:
                    elapsed_time = current_time - start_time
                    print(f"已擷取 {frame_count} 張影像，已用時間: {elapsed_time:.1f} 秒")
            
            cv2.imshow('Frame', frame)
            cv2.waitKey(1)
        
        cv2.destroyAllWindows()
        total_elapsed = time.time() - start_time
        print(f"\n擷取完成，共 {frame_count} 張影像，總用時: {total_elapsed:.1f} 秒")
        
        if similarities:
            person_indices = [s[0] for s in similarities]
            similarity_values = [s[1] for s in similarities]
            
            person_stats = {}
            for idx in set(person_indices):
                values = [v for i, v in enumerate(similarity_values) if person_indices[i] == idx]
                sorted_values = sorted(values)
                cut_size = len(sorted_values) // 10
                trimmed_values = sorted_values[cut_size:-cut_size]
                
                person_stats[idx] = {
                    'count': len(values),
                    'avg_similarity': np.mean(trimmed_values) if trimmed_values else 0
                }
            
            best_person = max(person_stats.items(), 
                            key=lambda x: (x[1]['count'], x[1]['avg_similarity']))
            
            return (best_person[0], best_person[1]['avg_similarity'])
        else:
            print("沒有有效的相似度數據")
            return None
        
    def calculate_similarity(self, processed_data):
        self.interpreter.set_tensor(self.input_details[0]['index'], processed_data)
        self.interpreter.invoke()
        prediction = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        
        brian_idx = self.labels.index('Brian')
        candy_idx = self.labels.index('Candy')
        
        brian_score = prediction[brian_idx]
        candy_score = prediction[candy_idx]
        
        print(f"Brian: {brian_score*100:.1f}%")
        print(f"Candy: {candy_score*100:.1f}%")
        
        if brian_score > candy_score:
            best_score = brian_score
            best_idx = brian_idx
        else:
            best_score = candy_score
            best_idx = candy_idx
        
        other_scores = [score for i, score in enumerate(prediction) if i not in [brian_idx, candy_idx]]
        if best_score > 0.5 and best_score > max(other_scores) * 1.2:
            print(f"\n偵測到 {self.labels[best_idx]}，相似度: {best_score*100:.1f}%")
            return (best_idx, best_score)
        else:
            print("\n未偵測到授權人員")
            return None