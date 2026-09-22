from gpiozero import AngularServo, Button
import time
from signal import pause

# サーボモーターの設定
servo = AngularServo(13, min_pulse_width=0.5/1000, min_angle=-90, \
                     max_pulse_width=2.4/1000, max_angle=90, \
                     frame_width=20.0/1000)

button = Button(26)

# 最初は0度（フタが閉まった状態）
current_angle = 0
servo.angle = current_angle
time.sleep(1)
servo.angle = None

# フタが開いているかどうかのフラグ
is_open = False

def move_slowly(target_angle):
    """ 指定した角度まで少しずつサーボを動かす関数 """
    global current_angle
    
    # 現在の角度から目標の角度まで1度ずつ動かす
    step = 3 if target_angle > current_angle else -3
    
    for angle in range(current_angle, target_angle + step, step):
        servo.angle = angle
        time.sleep(0.01) # ★この数値を大きくするともっとゆっくり動きます
        
    current_angle = target_angle
    
    # 動き終わったらジッター対策で信号を切る
    time.sleep(0.2)
    servo.angle = None

def toggle_lid():
    global is_open
    
    if not is_open:
        print("スイッチ検知：フタを90度開きます")
        move_slowly(90)   # 0度から90度へゆっくり動く
        is_open = True
    else:
        print("スイッチ検知：フタを0度へ閉じます")
        move_slowly(0)    # 90度から0度へゆっくり動く
        is_open = False

button.when_pressed = toggle_lid

print("プログラム起動中... スイッチを押すとゴミ箱のフタが開閉します（Ctrl+Cで終了）")

try:
    pause()
except KeyboardInterrupt:
    print("\nプログラムを終了します")
finally:
    servo.close()
