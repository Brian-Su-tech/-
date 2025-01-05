# 人臉辨識門禁系統

這是一個基於樹莓派的人臉辨識門禁系統，使用 OpenCV 進行人臉偵測和辨識。系統可以辨識授權人員，並透過 LINE Notify 發送通知。

## 系統功能

- 即時人臉偵測和辨識
- LED 狀態指示（黃色表示處理中、綠色表示通過、紅色表示未通過）
- LINE Notify 即時通知
- 自動儲存並分類照片
- 按鈕觸發辨識
- 網頁介面監控
- MySQL 資料庫記錄
- 歷史紀錄查詢功能

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
├── database.py                # 資料庫操作模組
├── utils.py                   # 工具函數
├── face.yml                   # 人臉模型檔
├── templates/                 # 網頁模板
│   ├── index.html            # 首頁模板
│   └── search.html           # 搜尋結果頁面
├── static/                   # 靜態檔案
│   ├── styles.css           # 首頁樣式
│   ├── styles2.css          # 搜尋頁面樣式
│   └── photos/              # 擷取的照片儲存位置
│       ├── brian/           # Brian 的照片
│       ├── candy/           # Candy 的照片
│       └── unknown/         # 未知人員的照片
└── opencv_test/             # OpenCV 測試和訓練工具
    ├── model.py             # 訓練模型程式
    ├── opencv.py            # OpenCV 測試程式
    ├── process_photos.py    # 照片處理工具
    └── photos/             # 訓練用照片
```

## 資料庫設定

1. 安裝 LAMP (Linux + Apache + MySQL + PHP) 環境：
```bash
# 安裝 Apache2
sudo apt install apache2

# 安裝 MySQL
sudo apt install mysql-server

# 安裝 PHP 和必要模組
sudo apt install php php-mysql php-common

# 安裝 phpMyAdmin
sudo apt install phpmyadmin
```

2. 設定 phpMyAdmin：
   - 安裝過程中選擇 Apache2
   - 設定 phpMyAdmin 資料庫管理員密碼
   - 訪問 `http://你的樹莓派IP/phpmyadmin` 進入管理介面

3. 使用 phpMyAdmin 建立資料庫和表格：
   - 登入 phpMyAdmin
   - 建立新資料庫 `face_rec`
   - 在 SQL 查詢視窗中執行：
```sql
CREATE TABLE recognition_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_name VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

4. 建立資料庫使用者：
   - 在 phpMyAdmin 中前往「使用者帳號」
   - 新增使用者 'face_user'@'localhost'
   - 設定密碼為 'user'
   - 勾選 face_rec 資料庫的所有權限
   - 點擊「執行」完成設定

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
pip install opencv-python numpy flask requests RPi.GPIO mysql-connector-python
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
   - 使用網頁介面查詢歷史紀錄

## 辨識流程

1. 按下按鈕後，黃色 LED 亮起表示開始處理
2. 系統擷取多張照片進行辨識
3. 辨識結果：
   - 成功：綠色 LED 亮起，LINE 通知顯示辨識到的人名
   - 失敗：紅色 LED 亮起，LINE 通知顯示辨識失敗
4. 照片自動儲存到對應的資料夾
5. 辨識結果記錄到資料庫
6. 5 秒後 LED 熄滅，系統回到待命狀態

## 網頁介面功能

- 顯示今日訪客數量
- 查看所有訪客紀錄
- 依據姓名和時間搜尋歷史照片
- 即時查看辨識結果

## 開發工具

- 訓練新的人臉模型：使用 `opencv_test/model.py`
- 測試 OpenCV 功能：使用 `opencv_test/opencv.py`
- 處理訓練照片：使用 `opencv_test/process_photos.py`

## 注意事項

- 系統預設辨識 "Brian" 和 "Candy" 兩個人物
- 辨識相似度閾值可在 config.py 中調整
- 確保攝影機正確連接且運作正常
- 需要網路連線才能使用 LINE 通知功能
- 確保 MySQL 服務正常運行
- 定期備份資料庫和照片資料