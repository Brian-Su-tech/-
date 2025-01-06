import cv2
import numpy as np
import os

# 使用 OpenCV 內建的分類器路徑
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
detector = cv2.CascadeClassifier(cascade_path)  # 載入人臉追蹤模型

# 確認分類器是否正確載入
if detector.empty():
    print("錯誤：無法載入人臉分類器")
    exit(1)

recog = cv2.face.LBPHFaceRecognizer_create()
faces = []
ids = []

# 讀取 brian 的照片（01-15）
for i in range(1, 16):
    img = cv2.imread(f'opencv_test/photos/brian/brian_{i:02d}.jpg')  # 使用 :02d 確保數字格式為 01, 02, ...
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 色彩轉換成黑白
    img_np = np.array(gray,'uint8')               # 轉換成指定編碼的 numpy 陣列
    face = detector.detectMultiScale(gray)        # 擷取人臉區域
    for(x,y,w,h) in face:
        faces.append(img_np[y:y+h,x:x+w])         # 記錄brian人臉的位置和大小內像素的數值
        ids.append(1)                             # 記錄brian人臉對應的 id，只能是整數，都是 1 表示brian的 id 為 1

# 讀取 trump 的照片（01-12）
for i in range(1, 13):
    img = cv2.imread(f'opencv_test/photos/candy/candy_{i:02d}.jpg')  # 使用 :02d 確保數字格式為 01, 02, ...
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 色彩轉換成黑白
    img_np = np.array(gray,'uint8')               # 轉換成指定編碼的 numpy 陣列
    face = detector.detectMultiScale(gray)        # 擷取人臉區域
    for(x,y,w,h) in face:
        faces.append(img_np[y:y+h,x:x+w])         # 記錄candy人臉的位置和大小內像素的數值
        ids.append(2)                             # 記錄candy人臉對應的 id，只能是整數，都是 2 表示candy的 id 為 2

print('training...')                              # 提示開始訓練
recog.train(faces,np.array(ids))                  # 開始訓練
recog.save('face.yml')                            # 訓練完成儲存為 face.yml
print('ok!')