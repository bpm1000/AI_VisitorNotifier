import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import requests
import openai
from tkinter import Tk, Label, Button

# OpenAI API設定
openai.api_key = 'Your-OpenAI-API-Key-Here'

# GPIO設定
GPIO.setmode(GPIO.BCM)
PIR_PIN = 17  # 人感センサーのGPIOピン番号
GPIO.setup(PIR_PIN, GPIO.IN)

# カメラ設定
camera = PiCamera()

# LINE Notify設定
LINE_TOKEN = 'Your-LINE-Notify-Token-Here'

def send_line_notify(message, image_path=None):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + LINE_TOKEN}
    payload = {'message': message}
    files = {'imageFile': open(image_path, 'rb')} if image_path else None
    try:
        r = requests.post(url, headers=headers, data=payload, files=files)
        r.raise_for_status()
        print("通知を送信しました")
    except requests.exceptions.RequestException as e:
        print(f"通知の送信に失敗しました: {e}")

def log_ai_response(response):
    with open('/home/pi/visitor_log.txt', 'a') as log:
        log.write(f"AI応答: {response}\n")

# GUI設定
def setup_gui():
    global gui_response_label
    root = Tk()
    root.title("訪問者ログ")
    
    visitor_label = Label(root, text="訪問者が検知されました")
    visitor_label.grid(row=0, column=0, columnspan=2)

    def handle_request(request_type):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"訪問者が来ました。要件は{request_type}です。次に何をしますか？"}
            ]
        )
        ai_response = response['choices'][0]['message']['content']
        print(ai_response)
        log_ai_response(ai_response)
        gui_response_label.config(text=f"AI応答: {ai_response}")

    Button(root, text="問い合わせ", command=lambda: handle_request("問い合わせ")).grid(row=1, column=0)
    Button(root, text="相談", command=lambda: handle_request("相談")).grid(row=1, column=1)
    gui_response_label = Label(root, text="")
    gui_response_label.grid(row=4, column=0, columnspan=2)

    root.mainloop()

# 人感センサーによる訪問者検知
def detect_visitor():
    print('PIRセンサー準備完了')
    time.sleep(2)
    print('検知開始')
    last_detection_time = 0
    debounce_time = 10  # 10秒間再検知を無視
    notified = False  # 通知を送信したかどうかを追跡
    sensor_triggered = False  # センサーが検知状態かどうかを追跡
    try:
        while True:
            if GPIO.input(PIR_PIN):
                current_time = time.time()
                if not notified and not sensor_triggered:
                    print('訪問者を検知')
                    image_path = '/home/pi/visitor.jpg'
                    camera.capture(image_path, resize=(800, 600))
                    send_line_notify('訪問者が検知されました。', image_path)
                    notified = True  # 通知を送信済みに設定
                    sensor_triggered = True  # センサーが検知状態に設定
                    last_detection_time = current_time
            else:
                sensor_triggered = False  # センサーが反応しなくなったら検知状態をリセット
                notified = False  # 通知フラグもリセット
            time.sleep(1)
    except KeyboardInterrupt:
        print('終了')
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    from threading import Thread
    gui_thread = Thread(target=setup_gui)
    detection_thread = Thread(target=detect_visitor)
    gui_thread.start()
    detection_thread.start()
    gui_thread.join()
    detection_thread.join()
