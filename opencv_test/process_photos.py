import os
from pathlib import Path

def rename_photos(folder_path):
    # 確保資料夾存在
    if not os.path.exists(folder_path):
        print(f"錯誤：找不到資料夾 '{folder_path}'")
        return

    # 取得所有 jpeg/jpg 檔案
    photo_files = []
    for ext in ('*.jpeg', '*.jpg'):
        photo_files.extend(Path(folder_path).glob(ext))
    
    # 排序檔案以確保順序一致
    photo_files.sort()
    
    # 重新命名檔案
    for index, photo in enumerate(photo_files, start=1):
        # 建立新檔名
        new_name = f"brian_{index:02d}.jpg"
        new_path = os.path.join(folder_path, new_name)
        
        try:
            photo.rename(new_path)
            print(f"已將 {photo.name} 重新命名為 {new_name}")
        except Exception as e:
            print(f"重新命名 {photo.name} 時發生錯誤：{str(e)}")

if __name__ == "__main__":
    # 指定 photos 資料夾的路徑
    photos_folder = "opencv_test/photos/brian"
    rename_photos(photos_folder)
