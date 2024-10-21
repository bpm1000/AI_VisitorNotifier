import RPi.GPIO as GPIO
import time

# GPIO設定
GPIO.setmode(GPIO.BCM)
PIR_PIN = 17
GPIO.setup(PIR_PIN, GPIO.IN)

print('PIRセンサー準備完了')
time.sleep(2)
print('検知開始')

try:
    while True:
        if GPIO.input(PIR_PIN):
            print('動きを検知しました')
            time.sleep(1)
        time.sleep(0.1)
except keybordInterrupt:
    print('終了')
finally:
    GPIO.cleanup()