# 人臉辨識門禁系統

這是一個基於樹莓派的人臉辨識門禁系統，使用 OpenCV 進行人臉偵測和辨識。系統可以辨識授權人員，並透過 LINE Notify 發送通知。

## 系統功能

- 即時人臉偵測和辨識
- LED 狀態指示（黃色表示處理中、綠色表示通過、紅色表示未通過）
- LINE Notify 即時通知
- 自動儲存並分類照片
- 按鈕觸發辨識
- 網頁介面監控

## 硬體需求

- 樹莓派 4B
- USB 攝影機
- LED 燈 (黃、綠、紅)
- 按鈕開關
- 杜邦線

## 接腳設定

- 黃色 LED: GPIO 11 (BOARD)
- 綠色 LED: GPIO 12 (BOARD)
- 紅色 LED: GPIO 13 (BOARD)
- 按鈕: GPIO 15 (BOARD)

## 檔案結構

```
├── main.py                     # 主程式進入點
├── config.py                   # 設定檔
├── face_recognition_system.py  # 人臉辨識系統核心
├── camera_processor.py         # 攝影機處理模組
├── led_controller.py          # LED 控制模組
├── line_notifier.py           # LINE 通知模組
├── utils.py                   # 工具函數
├── face.yml                   # 人臉模型檔
├── opencv_test/               # OpenCV 測試和訓練工具
│   ├── model.py              # 訓練模型程式
│   ├── opencv.py             # OpenCV 測試程式
│   └── process_photos.py     # 照片處理工具
└── captured_photos/           # 擷取的照片儲存位置
    ├── brian/                # Brian 的照片
    ├── candy/                # Candy 的照片
    └── unknown/              # 未知人員的照片
```

## 設定說明

1. 在 `config.py` 中設定：
   - GPIO 腳位
   - 相機參數
   - 辨識閾值
   - LINE Notify Token
   - Flask 網頁伺服器設定

2. 在 `face.yml` 中儲存訓練好的人臉模型

## 使用方法

1. 安裝相依套件：
```bash
pip install opencv-python numpy flask requests RPi.GPIO
```

2. 設定 LINE Notify Token：
   - 在 config.py 中填入你的 LINE Notify Token

3. 執行系統:
```bash
python main.py
```

4. 操作方式：
   - 按下按鈕開始辨識
   - 觀察 LED 燈號狀態
   - 查看 LINE 通知結果
   - 透過網頁介面監控系統

## 辨識流程

1. 按下按鈕後，黃色 LED 亮起表示開始處理
2. 系統擷取多張照片進行辨識
3. 辨識結果：
   - 成功：綠色 LED 亮起，LINE 通知顯示辨識到的人名
   - 失敗：紅色 LED 亮起，LINE 通知顯示辨識失敗
4. 照片自動儲存到對應的資料夾
5. 10 秒後 LED 熄滅，系統回到待命狀態

## 開發工具

- 訓練新的人臉模型：使用 `opencv_test/model.py`
- 測試 OpenCV 功能：使用 `opencv_test/opencv.py`
- 處理訓練照片：使用 `opencv_test/process_photos.py`

## 注意事項

- 系統預設辨識 "Brian" 和 "Candy" 兩個人物
- 辨識相似度閾值可在 config.py 中調整
- 確保攝影機正確連接且運作正常
- 需要網路連線才能使用 LINE 通知功能