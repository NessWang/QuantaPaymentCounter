import tkinter as tk
from tkinter import messagebox
import os
import sys

# ==== Step 1: 預設月薪設定為 None（系統會自動更新此行） ====
payment = None  # 自動寫入月薪

# ==== Step 2: 自我修改程式碼寫入薪資 ====
def set_payment_in_code(new_payment):
    script_path = os.path.abspath(__file__)
    with open(script_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith('payment = None'):
            lines[i] = f'payment = {new_payment}  # 自動寫入月薪\n'
            break

    with open(script_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

# ==== Step 3: 如果沒設定月薪，跳出視窗輸入 ====
if payment is None:
    def on_submit():
        try:
            entered_value = int(entry.get())
            if entered_value <= 0:
                raise ValueError
            set_payment_in_code(entered_value)
            messagebox.showinfo("設定完成", "月薪已寫入程式，下次執行會自動套用。\n請重新啟動程式。")
            root.destroy()
            sys.exit()
        except ValueError:
            messagebox.showerror("輸入錯誤", "請輸入正整數月薪")

    root = tk.Tk()
    root.title("首次執行 - 請輸入月薪")
    root.geometry("300x120")

    label = tk.Label(root, text="請輸入你的月薪（整數）：")
    label.pack(pady=5)

    entry = tk.Entry(root)
    entry.pack(pady=5)
    entry.focus()

    submit_button = tk.Button(root, text="確認", command=on_submit)
    submit_button.pack(pady=5)

    root.mainloop()
    sys.exit()

# ==== Step 4: 接下來寫你原本的主程式 ====

from tkinter import *
from tkinter import ttk
import time

# 工資相關計算
paymentday = payment / 22
paymenthour = paymentday / 9
paymentmin = paymenthour / 60
paymentsec = paymentmin / 60

paymentadd33day = ((payment / 240) * 1.33) * 2
paymentadd33hour = (payment / 240) * 1.33
paymentadd33min = paymentadd33hour / 60
paymentadd33sec = paymentadd33min / 60

paymentadd66day = ((payment / 240) * 1.66) * 2
paymentadd66hour = (payment / 240) * 1.66
paymentadd66min = paymentadd66hour / 60
paymentadd66sec = paymentadd66min / 60

# 全域變數
overtime_hours = 0.0
has_started = False
has_ended = False
selected_ot_button = None  # 紀錄目前選的按鈕
shutdown_counting = False
shutdown_after_id = None
flag1 = flag2 = flag3 = False
last_progress = 0  # 避免進度條歸零

FONT_DEFAULT = ("微軟正黑體", 12)
FONT_BOLD = ("微軟正黑體", 15, "bold")
FONT_BOLD_LARGE = ("微軟正黑體", 20, "bold")
FONT_BUTTON = ("微軟正黑體", 10, "bold")

def get_work_and_off_times():
    try:
        wh = work_hour.get()
        wm = work_minute.get()
        wuh = int(workup_hour.get())
        wum = int(workup_minute.get())
    except ValueError:
        return None, None
    today_str = time.strftime('%Y-%m-%d')

    # 判斷下班時間是否為隔日（00）
    if wh == '00':
        # 隔日，加一天
        off_date = time.localtime(time.mktime(time.strptime(today_str, "%Y-%m-%d")) + 86400)
        off_str = f"{off_date.tm_year}-{off_date.tm_mon:02d}-{off_date.tm_mday:02d} 00:{wm}:00"
    else:
        off_str = f"{today_str} {wh}:{wm}:00"

    up_str = f"{today_str} {wuh:02d}:{wum:02d}:00"

    try:
        off_time = time.mktime(time.strptime(off_str, "%Y-%m-%d %H:%M:%S"))
        up_time = time.mktime(time.strptime(up_str, "%Y-%m-%d %H:%M:%S"))
    except Exception:
        return None, None
    return off_time, up_time

def start_shutdown_timer():
    global shutdown_counting, shutdown_after_id
    shutdown_counting = True

    def countdown_and_blink(countdown):
        global shutdown_after_id, shutdown_counting
        if countdown < 0:
            shutdown_counting = False
            shutdown_after_id = None
            shutdown_label.config(text="倒數結束")
            set_led_color('gray')
            tk_obj.quit()  # 自動關閉視窗（或用 tk_obj.after(0, tk_obj.destroy)）
            return
        color = 'red' if countdown % 2 == 0 else 'white'
        set_led_color(color)
        shutdown_label.config(text=f"{countdown}")
        shutdown_after_id = tk_obj.after(1000, countdown_and_blink, countdown - 1)

    countdown_and_blink(300)

def stop_shutdown_timer():
    global shutdown_after_id, shutdown_counting
    if shutdown_after_id is not None:
        tk_obj.after_cancel(shutdown_after_id)
        shutdown_after_id = None
    shutdown_counting = False
    shutdown_label.config(text="")
    set_led_color('green')

def update_countdown():
    global has_ended, flag1, flag2, flag3, last_progress
    if not has_started or has_ended:
        return  # 不重設進度條為0，避免閃爍

    now = time.time()
    off_time, up_time = get_work_and_off_times()
    if off_time is None or up_time is None:
        down_label.config(text="時間格式錯誤")
        return

    diff = int(off_time - now) + 1

    if diff == 3:
        flag1 = True
    elif diff == 2:
        flag2 = True
    elif diff == 1:
        flag3 = True

    if flag1 and flag2 and flag3 and not shutdown_counting:
        start_shutdown_timer()

    if diff <= 0:
        down_label.config(text="已到下班時間")
        has_ended = True
        progress_var.set(100)
        last_progress = 100
        set_led_color('gray')
    else:
        h = diff // 3600
        m = (diff % 3600) // 60
        s = diff % 60
        down_label.config(text=f"{h:02d}時{m:02d}分{s:02d}秒")
        total_sec = off_time - up_time
        elapsed_sec = now - up_time
        if elapsed_sec < 0:
            elapsed_sec = 0
        progress = int((elapsed_sec / total_sec) * 100) if total_sec > 0 else 0
        progress = min(progress, 100)
        if progress != last_progress:
            progress_var.set(progress)
            last_progress = progress
        set_led_color('green')
        tk_obj.after(1000, update_countdown)

def update_money():
    global has_ended
    if not has_started or has_ended:
        return
    now = time.time()
    off_time, up_time = get_work_and_off_times()
    if off_time is None or up_time is None:
        return
    diffup_time = now - up_time
    if diffup_time < 0:
        money_label.config(text="$0.00")
    else:
        if diffup_time > 41400:
            money = paymentday + paymentadd33day + (diffup_time - 41400) * paymentadd66sec
        elif diffup_time > 34200:
            money = paymentday + (diffup_time - 34200) * paymentadd33sec
        elif diffup_time > 32400:
            money = paymentday
        else:
            money = diffup_time * paymentsec
        money_label.config(text=f"${money:.2f}")
        tk_obj.after(100, update_money)

def refresh_current_time():
    curr_time.config(text=time.strftime('%Y-%m-%d %H:%M:%S'))
    tk_obj.after(1000, refresh_current_time)

def set_overtime(hour, button):
    global overtime_hours, selected_ot_button
    overtime_hours = hour
    if selected_ot_button:
        selected_ot_button.config(bg='#388e3c')
    button.config(bg='#2e7d32')
    selected_ot_button = button

    try:
        wuh = int(workup_hour.get())
        wum = int(workup_minute.get())
    except ValueError:
        return
    base_hours = 9.0
    if hour > 0:
        base_hours += 0.5 + hour
    total_sec = base_hours * 3600
    up_time = time.mktime(time.strptime(f"{time.strftime('%Y-%m-%d')} {wuh:02d}:{wum:02d}:00", "%Y-%m-%d %H:%M:%S"))
    new_off_time = up_time + total_sec
    new_off_struct = time.localtime(new_off_time)
    work_hour.set(f"{new_off_struct.tm_hour:02d}")
    work_minute.set(f"{new_off_struct.tm_min:02d}")
    start_all()  # 加班時間改變後自動重啟

def clean_and_start():
    global overtime_hours, has_started, has_ended, selected_ot_button
    global flag1, flag2, flag3
    overtime_hours = 0.0
    has_started = True
    has_ended = False
    flag1 = False
    flag2 = False
    flag3 = False
    stop_shutdown_timer()  # 停止倒數關閉紅燈閃爍，指示燈變綠

    if selected_ot_button:
        selected_ot_button.config(bg='#388e3c')
    selected_ot_button = None
    try:
        wuh = int(workup_hour.get())
        wum = int(workup_minute.get())
    except ValueError:
        return
    today_str = time.strftime('%Y-%m-%d')
    up_time = time.mktime(time.strptime(f"{today_str} {wuh:02d}:{wum:02d}:00", "%Y-%m-%d %H:%M:%S"))
    nine_hours_later = up_time + 9 * 3600
    eighteen_time = time.mktime(time.strptime(f"{today_str} 18:00:00", "%Y-%m-%d %H:%M:%S"))
    off_time = min(nine_hours_later, eighteen_time)
    off_struct = time.localtime(off_time)
    work_hour.set(f"{off_struct.tm_hour:02d}")
    work_minute.set(f"{off_struct.tm_min:02d}")
    start_all()

def start_all():
    global has_started, has_ended
    has_started = True
    has_ended = False
    now = time.time()
    off_time, up_time = get_work_and_off_times()
    if off_time is None or up_time is None:
        return

    if now > off_time:
        # 已超過下班時間，直接計算薪資並顯示，不啟動倒數
        diffup_time = off_time - up_time
        if diffup_time > 41400:
            money = paymentday + paymentadd33day + (diffup_time - 41400) * paymentadd66sec
        elif diffup_time > 34200:
            money = paymentday + (diffup_time - 34200) * paymentadd33sec
        elif diffup_time > 32400:
            money = paymentday
        else:
            money = diffup_time * paymentsec
        money_label.config(text=f"${money:.2f}")
        down_label.config(text="已到下班時間")
        has_ended = True
        progress_var.set(100)
        set_led_color('gray')
        return

    # 尚未到下班時間，開始正常倒數與薪資計算
    update_countdown()
    update_money()

#檢查有無輸入Payment
def check_payment():
    try:
        if float(payment) <= 0:
            raise ValueError
    except:
        warning_win = Toplevel()
        warning_win.title("警告")
        warning_win.geometry("280x120")
        warning_win.resizable(False, False)
        warning_win.config(bg="white")
        warning_win.iconbitmap('Dog.ico')

        Label(warning_win, text="⚠ 請先正確設定月薪金額！", font=("微軟正黑體", 12), fg="red", bg="white").pack(pady=20)

        Button(warning_win, text="關閉", font=("微軟正黑體", 10), width=10,
               bg="#d32f2f", fg="white", command=warning_win.destroy).pack()

        # 暫停主視窗直到使用者關閉此視窗
        warning_win.transient(tk_obj)
        warning_win.grab_set()
        tk_obj.wait_window(warning_win)
# GUI
tk_obj = Tk()
tk_obj.geometry('400x400')
tk_obj.resizable(0, 0)
tk_obj.config(bg='white')
tk_obj.title('倒數計時應用')
tk_obj.iconbitmap('Dog.ico')  # 請自行放置icon路徑或註解此行

# 美化圓形指示燈，改用 Canvas
led_canvas = Canvas(tk_obj, width=20, height=20, bg='white', highlightthickness=0)
led_canvas.place(x=10, y=10)
led_circle = led_canvas.create_oval(2, 2, 18, 18, fill='green', outline='gray')

def set_led_color(color):
    led_canvas.itemconfig(led_circle, fill=color)

shutdown_label = Label(tk_obj, text='', font=('微軟正黑體', 10), fg='red', bg='white')
shutdown_label.place(x=35, y=8)

Label(tk_obj, text='下班倒數計時', font=FONT_BOLD_LARGE, bg='white').pack()
Label(tk_obj, font=FONT_BOLD, text='當前時間：', bg='white').place(x=50, y=50)
curr_time = Label(tk_obj, font=FONT_DEFAULT, text='', fg='gray25', bg='white')
curr_time.place(x=160, y=50)

Label(tk_obj, font=FONT_BOLD, text='上班時間：', bg='white').place(x=50, y=85)
workup_hour = StringVar()
workup_minute = StringVar()
hour_choices = [f"{h:02d}" for h in range(7, 18)]  # 上班時段7~17點
minute_choices = [f"{m:02d}" for m in range(60)]
ttk.Combobox(tk_obj, textvariable=workup_hour, values=hour_choices, width=3, state='readonly', font=FONT_DEFAULT).place(x=160, y=90)
ttk.Combobox(tk_obj, textvariable=workup_minute, values=minute_choices, width=3, state='readonly', font=FONT_DEFAULT).place(x=205, y=90)
workup_hour.set('09')
workup_minute.set('00')

Label(tk_obj, font=FONT_BOLD, text='下班時間：', bg='white').place(x=50, y=120)
work_hour = StringVar()
work_minute = StringVar()
hour_choices_full = [f"{h:02d}" for h in range(7, 24)] + ['00']  # 下班時段7~23點 + 00(隔日)

# 下班時間時、分 Combobox 改成變數，並綁定事件觸發 start_all
cb_wh = ttk.Combobox(tk_obj, textvariable=work_hour, values=hour_choices_full, width=3, state='readonly', font=FONT_DEFAULT)
cb_wh.place(x=160, y=125)
cb_wh.bind("<<ComboboxSelected>>", lambda e: start_all())

cb_wm = ttk.Combobox(tk_obj, textvariable=work_minute, values=minute_choices, width=3, state='readonly', font=FONT_DEFAULT)
cb_wm.place(x=205, y=125)
cb_wm.bind("<<ComboboxSelected>>", lambda e: start_all())

work_hour.set('18')
work_minute.set('00')

# 跨日提示
cross_day_label = Label(tk_obj, font=("微軟正黑體", 10), text="", fg='red', bg='white')
cross_day_label.place(x=270, y=130)

Label(tk_obj, font=FONT_BOLD, text='剩餘時間：', bg='white').place(x=50, y=160)
down_label = Label(tk_obj, font=("微軟正黑體", 16), text='00時00分00秒', fg='gray25', bg='white')
down_label.place(x=160, y=160)

Label(tk_obj, font=FONT_BOLD, text='今日錢錢：', bg='white').place(x=50, y=195)
money_label = Label(tk_obj, font=("微軟正黑體", 16), text='$0.00', fg='gray25', bg='white')
money_label.place(x=160, y=195)

Label(tk_obj, text='加班：', font=FONT_BOLD, bg='white').place(x=50, y=230)
btn_frame = Frame(tk_obj, bg='white')
btn_frame.place(x=110, y=230)

ot_hours = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
ot_buttons = []
for i, h in enumerate(ot_hours):
    def make_lambda(hh=h, btn_idx=i):
        return lambda: set_overtime(hh, ot_buttons[btn_idx])
    btn = Button(btn_frame, text=f"+{h}h", width=5,
                 font=FONT_BUTTON,
                 bg='#388e3c', fg='white', relief='flat')
    btn.config(command=make_lambda())
    btn.grid(row=i // 4, column=i % 4, padx=2, pady=2)
    ot_buttons.append(btn)

start_btn = Button(tk_obj, text='START', bd=5, command=start_all,
                   bg='#388e3c', fg='white', font=FONT_BUTTON, relief='flat')
start_btn.place(x=140, y=310)

clean_btn = Button(tk_obj, text='CLEAN', bd=5, command=clean_and_start,
                   bg='#f57c00', fg='white', font=FONT_BUTTON, relief='flat')
clean_btn.place(x=220, y=310)

progress_var = IntVar()
progress_bar = ttk.Progressbar(tk_obj, orient=HORIZONTAL, length=300, mode='determinate', variable=progress_var)
progress_bar.place(x=60, y=360)

def update_cross_day_label():
    # 判斷是否跨日
    wh = work_hour.get()
    if wh == '00':
        cross_day_label.config(text="(已跨日)")
    else:
        cross_day_label.config(text="")
    tk_obj.after(1000, update_cross_day_label)

update_cross_day_label()
refresh_current_time()
check_payment()  # 啟動前檢查 payment 是否正確
tk_obj.mainloop()


# 在這裡開始你的主程式邏輯，例如開啟 tkinter UI 等...
