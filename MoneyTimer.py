from tkinter import *
import time
import os
import math
#from playsound import playsound
mp3File = "TimeUp.mp3"


def refresh_current_time():
    """重新整理當前時間"""
    global timer
    global diff_time
    clock_time = time.strftime('%Y-%m-%d %H:%M:%S')
    curr_time.config(text=clock_time)
    if timer > -1:
        timer += 1
        if timer == 300: #幾秒後關閉程式
            exit()
    curr_time.after(1000, refresh_current_time)


def refresh_down_time():
    """重新整理倒數計時時間"""
    # 當前時間戳
    global diff_time
    global timer
    payment = #在此輸入薪資
    paymentday = float((payment/22))
    paymenthour = float(paymentday/9)
    paymentmin = float(paymenthour/60)
    paymentsec = float(paymentmin/60)
#加班算法-----------------------------------------------------
    paymentadd33day = float(((payment/240)*1.33)*2)
    paymentadd33hour = float((payment/240)*1.33)
    paymentadd33min = float(paymentadd33hour/60)
    paymentadd33sec = float(paymentadd33min/60)
    paymentadd66day = float(((payment/240)*1.66)*2)
    paymentadd66hour = float((payment/240)*1.66)
    paymentadd66min = float(paymentadd66hour/60)
    paymentadd66sec = float(paymentadd66min/60)
    now_time = int(time.time())
    # 下班時間時分秒資料過濾
    work_hour_val = int(work_hour.get())
    if work_hour_val > 23:
        down_label.config(text='小時的區間為（00-23）')
        return
    work_minute_val = int(work_minute.get())
    if work_minute_val > 59:
        down_label.config(text='分鐘的區間為（00-59）')
        return
    work_second_val = int(work_second.get())
    if work_second_val > 59:
        down_label.config(text='秒數的區間為（00-59）')
        return
    # 上班時間時分秒資料過濾
    workup_hour_val = int(workup_hour.get())
    if workup_hour_val > 23:
        down_label.config(text='小時的區間為（00-23）')
        return
    workup_minute_val = int(workup_minute.get())
    if workup_minute_val > 59:
        down_label.config(text='分鐘的區間為（00-59）')
        return
    workup_second_val = int(workup_second.get())
    if workup_second_val > 59:
        down_label.config(text='秒數的區間為（00-59）')
        return
    # 下班時間轉為時間戳
    work_date = str(work_hour_val) + ':' + str(work_minute_val) + ':' + str(work_second_val)
    work_str_time = time.strftime('%Y-%m-%d ') + work_date
    time_array = time.strptime(work_str_time, "%Y-%m-%d %H:%M:%S")
    work_time = time.mktime(time_array)
    # 上班時間轉為時間戳
    workup_date = str(workup_hour_val) + ':' + str(workup_minute_val) + ':' + str(workup_second_val)
    workup_str_time = time.strftime('%Y-%m-%d ') + workup_date
    timeup_array = time.strptime(workup_str_time, "%Y-%m-%d %H:%M:%S")
    workup_time = time.mktime(timeup_array)
    if now_time > work_time:
        down_label.config(text='已過下班時間')
        if diffup_time>41400:
            money_label.config(text='$%d'%(paymentday+paymentadd33day+paymentadd66day))
            print("diffup_time1= %d"%diffup_time)
        else:
            if diffup_time > 34200:
                money_label.config(text='$%d'%(paymentday+paymentadd33day))
                print("diffup_time2= %d"%diffup_time)
            else:
                if diffup_time > 32400:
                    money_label.config(text='$%d'%paymentday)
                    print("diffup_time3= %d"%diffup_time)
                else:
                    ccc = math.ceil((32400-(work_time-workup_time))/3600)
                    money_label.config(text='$%d '%paymentday+'扣掉 $%d'%(120.8333*ccc)+'\n需要請假%d小時'%ccc)
                    print("diffup_time4= %d"%diffup_time)
        return
    # 距離下班時間剩餘秒數
    diff_time = int(work_time - now_time)
    while diff_time > -1:
        # 獲取倒數計時-時分秒
        now_time = int(time.time())
        diff_time = int(work_time - now_time) #2022/12/14測試 每秒都校正時間
        diffup_time = int(now_time - workup_time) #2022/12/14測試 每秒都校正時間
        down_minute = diff_time // 60
        down_second = diff_time % 60
        down_hour = 0
        if down_minute >= 60:
            down_hour = down_minute // 60
            down_minute = down_minute % 60
        # 重新整理倒數計時時間
        down_time = str(down_hour).zfill(2) + '時' + str(down_minute).zfill(2) + '分' + str(down_second).zfill(2) + '秒'
        tk_obj.update()
        '''
        if diff_time <= 120 and diff_time > 0: #倒數兩分鐘時播放音效
            down_label.config(text=down_time+'\n'+'時間快到了')
            if timeup == 0:
                playsound(mp3File)
                timeup == 1 #播放一次後Flag舉起
        else:
            down_label.config(text=down_time)
        '''
        down_label.config(text=down_time)
        
        if diff_time < 0:
            # 倒數計時結束
            down_label.config(text='已到下班時間')
            diffup_time = int(work_time - workup_time)
            if diffup_time>41400:
                money_label.config(text='$%d'%(paymentday+paymentadd33day+paymentadd66day))
                print("diffup_time1= %d"%diffup_time)
            else:
                if diffup_time > 34200:
                    money_label.config(text='$%d'%(paymentday+paymentadd33day))
                    print("diffup_time2= %d"%diffup_time)
                else:
                    if diffup_time > 32400:
                        money_label.config(text='$%d'%(paymentday))
                        print("diffup_time3= %f"%diffup_time)
                    else:
                        money_label.config(text='$%d'%(paymentday))
                        print("diffup_time4= %f"%diffup_time)
            print("Break!!!!!!!!!!")
            timer = 0
            break
        #print("diff_time=%d"%diff_time)
        #print("diffup_time=%d"%diffup_time)
        for x in range(10):
            if diffup_time > 41400:
                money = float(paymentday+paymentadd33day+(diffup_time-41400)*paymentadd66sec) #超過4小時也可以計算
            else:
                if diffup_time > 34200:
                    money = float(paymentday+(diffup_time-34200)*paymentadd33sec)
                else:
                    if diffup_time > 32400:
                        money = float(paymentday)
                    else:
                        money = float((diffup_time)*paymentsec)
            money_label.config(text='$'+"%.2f"%money)
            time.sleep(0.1)
            diffup_time += 0.1
            tk_obj.update()
#            diff_time -= 1 #每秒校正後就不需要每秒-1
# 程式主入口
if __name__ == "__main__":
    # 設定頁面資料
    tk_obj = Tk()
    tk_obj.geometry('400x330')
    tk_obj.resizable(0, 0)
    tk_obj.config(bg='white')
    tk_obj.title('倒數計時應用')
    tk_obj.iconbitmap('Dog.ico')
    global timer
    timer = -1
    Label(tk_obj, text='下班倒數計時', font='宋體 20 bold', bg='white').pack()
    # 設定當前時間
    Label(tk_obj, font='宋體 15 bold', text='當前時間：', bg='white').place(x=50, y=60)
    curr_time = Label(tk_obj, font='宋體 15', text='', fg='gray25', bg='white')
    curr_time.place(x=160, y=60)
    refresh_current_time()
    # 設定下班時間
    Label(tk_obj, font='宋體 15 bold', text='下班時間：', bg='white').place(x=50, y=150)
    # 下班時間-小時
    work_hour = StringVar()
    Entry(tk_obj, textvariable=work_hour, width=2, font='宋體 12').place(x=160, y=155)
    work_hour.set('18')
    # 下班時間-分鐘
    work_minute = StringVar()
    Entry(tk_obj, textvariable=work_minute, width=2, font='宋體 12').place(x=185, y=155)
    work_minute.set('00')
    # 下班時間-秒數
    work_second = StringVar()
    Entry(tk_obj, textvariable=work_second, width=2, font='宋體 12').place(x=210, y=155)
    work_second.set('00')

    # 設定上班時間
    Label(tk_obj, font='宋體 15 bold', text='上班時間：', bg='white').place(x=50, y=115)
    # 上班時間-小時
    workup_hour = StringVar()
    Entry(tk_obj, textvariable=workup_hour, width=2, font='宋體 12').place(x=160, y=120)
    workup_hour.set('09')
    # 上班時間-分鐘
    workup_minute = StringVar()
    Entry(tk_obj, textvariable=workup_minute, width=2, font='宋體 12').place(x=185, y=120)
    workup_minute.set('00')
    # 上班時間-秒數
    workup_second = StringVar()
    Entry(tk_obj, textvariable=workup_second, width=2, font='宋體 12').place(x=210, y=120)
    workup_second.set('00')
    # 設定剩餘時間
    Label(tk_obj, font='宋體 15 bold', text='剩餘時間：', bg='white').place(x=50, y=190) #原本y=160
    down_label = Label(tk_obj, font='宋體 16', text='', fg='gray25', bg='white')
    down_label.place(x=160, y=190) #原本y=160
    down_label.config(text='00時00分00秒')
    # 設定賺到的錢錢
    Label(tk_obj, font='宋體 15 bold', text='今日錢錢：', bg='white').place(x=50, y=230)
    money_label = Label(tk_obj, font='宋體 16', text='', fg='gray25', bg='white')
    money_label.place(x=160, y=230) #原本y=160
    money_label.config(text='$'+'0')

    # 開始計時按鈕
    Button(tk_obj, text='START', bd='5', command=refresh_down_time, bg='green', font='宋體 10 bold').place(x=155, y=282)
    tk_obj.mainloop()
