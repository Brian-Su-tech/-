# 樹莓派人臉辨識系統

這是一個基於樹莓派的人臉辨識系統，使用 TensorFlow Lite 進行人臉辨識，並整合了 LINE Notify 通知功能和 LED 指示燈顯示辨識結果。

## 功能特點

- 即時人臉辨識
- LINE Notify 通知功能
- LED 狀態指示
- 網頁介面
- 按鈕觸發辨識
- 高準確度的辨識演算法

## 硬體需求

- 樹莓派（建議使用 Raspberry Pi 4）
- 攝影機模組
- LED 燈 x3（黃、綠、紅）
- 按鈕開關
- 杜邦線和麵包板

## GPIO 接腳配置

- 黃色 LED：GPIO 11
- 綠色 LED：GPIO 12
- 紅色 LED：GPIO 13
- 按鈕：GPIO 15

## 軟體需求

- Python 3.7+
- OpenCV
- TensorFlow Lite
- RPi.GPIO
- Flask
- requests

## 安裝步驟

1. 克隆專案
2. 安裝相依套件
3. 設定 LINE Notify 的 token
4. 設定 config.py 中的相關參數
5. 執行 main.py

## 系統設定

可在 `config.py` 中調整以下參數：
- 辨識相似度閾值
- 擷取時間
- 目標影格數
- 檢查間隔
- Flask 伺服器設定

## LED 指示燈說明

- 黃燈：系統正在處理影像
- 綠燈：辨識成功且通過
- 紅燈：辨識失敗或未通過

## 網頁介面

系統提供簡單的網頁介面，可通過以下網址存取：