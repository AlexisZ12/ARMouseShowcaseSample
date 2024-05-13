import cv2
import numpy as np
import HandTrackingModule as htm
import autopy
from pynput import mouse, keyboard
import tkinter as tk
import keyboard as listener
import sys

# 关闭tkinter窗口函数
def hit_sure():
    W_AR.destroy()



# 初始化数值
wCam, hCam = 640, 480   # 摄像头宽度
wScr, hScr = autopy.screen.size()   # 获取屏幕尺寸
frameR = 150   # 摄像头边框宽度
smoothening = 7   # 平滑度
sense = 3   # 灵敏度
plocX, plocY = 0, 0
clocX, clocY = 0, 0
flag_change = 0   # 手势是否改变
flag_click = 0   # 左键是否按下
fingers = [0, 0, 0, 0, 0]   # 当前手势
fingers_old = [0, 0, 0, 0, 0]   # 上一个手势
y4 = wScr / 2
y4_old = wScr / 2
flag_updown = 0
info = [0, 0, 0, 0, 0]
index_up = 30
index_down = 30
operator = keyboard.Controller()
control = mouse.Controller()



# tkinter窗口信息
W_AR=tk.Tk()
W_AR.title('ARmouse')
W_AR.geometry('800x400')
W_AR.iconbitmap('icon.ico')



# tkinter定义变量
var_1 = tk.StringVar()
var_2 = tk.StringVar()
var_flag1 = tk.StringVar()
var_flag2 = tk.StringVar()
var_flag3 = tk.StringVar()
var_flag4 = tk.StringVar()
var_flag5 = tk.StringVar()
var_flag6 = tk.StringVar()



# tkinter变量默认值
var_1.set(sense)   #设置灵敏度
var_2.set(frameR)   #设置平滑度
var_flag1.set(1)
var_flag2.set(1)
var_flag3.set(1)
var_flag4.set(1)
var_flag5.set(1)
var_flag6.set(1)



# tkinter窗口布局
L_1 = tk.Label(W_AR, text='灵敏度', font=('等线', 24)).place(anchor='nw', relx=0.025, rely=0, relwidth=0.2, relheight=0.2)
L_2 = tk.Label(W_AR, text='边框宽度', font=('等线', 24)).place(anchor='nw', relx=0.025, rely=0.2, relwidth=0.2, relheight=0.2)
L_3 = tk.Label(W_AR, text='显示操作', font=('等线', 24)).place(anchor='nw', relx=0.025, rely=0.4, relwidth=0.2, relheight=0.2)
L_4 = tk.Label(W_AR, text='监视器', font=('等线', 24)).place(anchor='nw', relx=0.025, rely=0.6, relwidth=0.2, relheight=0.2)

E_1 = tk.Entry(W_AR, show=None, font=('等线', 24), textvariable=var_1).place(anchor='nw', relx=0.275, rely=0.02, relwidth=0.2, relheight=0.16)
E_2 = tk.Entry(W_AR, show=None, font=('等线', 24), textvariable=var_2).place(anchor='nw', relx=0.275, rely=0.22, relwidth=0.2, relheight=0.16)
R_1 = tk.Radiobutton(W_AR, text='开', font=('等线', 24), variable=var_flag1, value='1').place(anchor='nw', relx=0.275, rely=0.42, relwidth=0.1, relheight=0.16)
R_2 = tk.Radiobutton(W_AR, text='关', font=('等线', 24), variable=var_flag1, value='0').place(anchor='nw', relx=0.375, rely=0.42, relwidth=0.1, relheight=0.16)
R_3 = tk.Radiobutton(W_AR, text='开', font=('等线', 24), variable=var_flag2, value='1').place(anchor='nw', relx=0.275, rely=0.62, relwidth=0.1, relheight=0.16)
R_4 = tk.Radiobutton(W_AR, text='关', font=('等线', 24), variable=var_flag2, value='0').place(anchor='nw', relx=0.375, rely=0.62, relwidth=0.1, relheight=0.16)

L_5 = tk.Label(W_AR, text='单击功能', font=('等线', 24)).place(anchor='nw', relx=0.525, rely=0, relwidth=0.2, relheight=0.2)
L_6 = tk.Label(W_AR, text='双击功能', font=('等线', 24)).place(anchor='nw', relx=0.525, rely=0.2, relwidth=0.2, relheight=0.2)
L_7 = tk.Label(W_AR, text='滑动功能', font=('等线', 24)).place(anchor='nw', relx=0.525, rely=0.4, relwidth=0.2, relheight=0.2)
L_8 = tk.Label(W_AR, text='右键手势', font=('等线', 24)).place(anchor='nw', relx=0.525, rely=0.6, relwidth=0.2, relheight=0.2)

R_5 = tk.Radiobutton(W_AR, text='开', font=('等线', 24), variable=var_flag3, value='1').place(anchor='nw', relx=0.775, rely=0.02, relwidth=0.1, relheight=0.16)
R_6 = tk.Radiobutton(W_AR, text='关', font=('等线', 24), variable=var_flag3, value='0').place(anchor='nw', relx=0.875, rely=0.02, relwidth=0.1, relheight=0.16)
R_7 = tk.Radiobutton(W_AR, text='开', font=('等线', 24), variable=var_flag4, value='1').place(anchor='nw', relx=0.775, rely=0.22, relwidth=0.1, relheight=0.16)
R_8 = tk.Radiobutton(W_AR, text='关', font=('等线', 24), variable=var_flag4, value='0').place(anchor='nw', relx=0.875, rely=0.22, relwidth=0.1, relheight=0.16)
R_9 = tk.Radiobutton(W_AR, text='开', font=('等线', 24), variable=var_flag5, value='1').place(anchor='nw', relx=0.775, rely=0.42, relwidth=0.1, relheight=0.16)
R_10 = tk.Radiobutton(W_AR, text='关', font=('等线', 24), variable=var_flag5, value='0').place(anchor='nw', relx=0.875, rely=0.42, relwidth=0.1, relheight=0.16)
R_11 = tk.Radiobutton(W_AR, text='OK', font=('等线', 24), variable=var_flag6, value='1').place(anchor='nw', relx=0.775, rely=0.62, relwidth=0.1, relheight=0.16)
R_12 = tk.Radiobutton(W_AR, text='六', font=('等线', 24), variable=var_flag6, value='0').place(anchor='nw', relx=0.875, rely=0.62, relwidth=0.1, relheight=0.16)

sure = tk.Button(W_AR, text='确认', font=('等线', 24), command=hit_sure).place(anchor='nw', relx=0.4, rely=0.82, relwidth=0.2, relheight=0.16)



# 启动窗口
W_AR.mainloop()



# 设置右键手势
if var_flag6.get() == '0':
    finger_RC = [1, 0, 0, 0, 1]
else:
    finger_RC = [0, 0, 1, 1, 1]



# 启动摄像头
cap = cv2.VideoCapture(1)   # 调用摄像头
cap.set(3, wCam)   # 设置宽度
cap.set(4, hCam)   # 设置高度



# 加载手部检测模型
detector = htm.handDetector(maxHands=1)



while True:
    success, img = cap.read()   # 读取图像
    img = detector.findHands(img)   # 找到手
    lmList, bbox = detector.findPosition(img)   # 手指坐标位置
    fingers = detector.fingersUp()   # 手指是否伸出



    if len(lmList) != 0:
        x1, y1 = lmList[4][1:]   # 拇指指尖坐标
        x2, y2 = lmList[8][1:]   # 食指指尖坐标
        y4_new = int((y1 + y2) / 2)



    # 左键按下
    if fingers == [0, 1, 0, 0, 0] and flag_change == 1:
        control.press(mouse.Button.left)
        flag_click = 1
        info[4] = 10



    # 左键单击
    if var_flag3.get() == '1':
        if fingers == [1, 0, 1, 1, 1] and flag_change == 1:
            control.click(mouse.Button.left, 1)
            info[4] = 10



    # 左键双击
    if var_flag4.get() == '1':
        if fingers == [0, 1, 1, 0, 0] and flag_change == 1:
            control.click(mouse.Button.left, 2)
            info[0] = 10



    # 右键
    if fingers == finger_RC and flag_change == 1:
        control.click(mouse.Button.right, 1)
        info[1] = 10



    # 移动鼠标
    if fingers == [1, 1, 1, 1, 1] or flag_click == 1:
        
        # 获取手掌坐标
        x_center = int((lmList[0][1] + lmList[5][1] + lmList[17][1]) / 3)   # 计算出手掌中心横坐标
        y_center = int((lmList[0][2] + lmList[5][2] + lmList[17][2]) / 3)   # 计算出手掌中心纵坐标
        
        # 坐标转换
        x = np.interp(x_center, (frameR, wCam - frameR), (0, wScr))   # 坐标映射，用于将摄像头边框设置为死区
        y = np.interp(y_center, (frameR, hCam - frameR), (0, hScr))
        x = max(1, min(x, wScr-1))   # 限制取值范围，确保取值在屏幕范围内
        y = max(1, min(y, hScr-1))
        
        # 平滑处理坐标值
        clocX = plocX + (x - plocX) / smoothening
        clocY = plocY + (y - plocY) / smoothening
        
        # 移动鼠标
        # autopy.mouse.move(wScr - clocX, clocY)
        control.position = (wScr - clocX, clocY)
        
        # 绘制手掌中心点
        cv2.circle(img, (x_center, y_center), 15, (255, 0, 255), cv2.FILLED)
        
        # 更新数据
        plocX, plocY = clocX, clocY
    


    # 向上滚动
    if var_flag5.get() == '1':
        if (fingers == [1, 1, 1, 1, 1] or fingers == [0, 1, 1, 1, 1]) and index_up < sense:
            operator.press(keyboard.Key.up)
            operator.release(keyboard.Key.up)
            index_up = sense
            info[2] = 10

    # 向下滚动
    if var_flag5.get() == '1':
        if (fingers == [0, 0, 0, 0, 0] or fingers == [1, 0, 0, 0, 0]) and index_down < sense:
            operator.press(keyboard.Key.down)
            operator.release(keyboard.Key.down)
            index_down = sense
            info[3] = 10



    # 检测手势是否改变
    if fingers == fingers_old:
        flag_change = 0
    else:
        flag_change = 1
        flag_click = 0
        control.release(mouse.Button.left)
    fingers_old = fingers

    if fingers == [0, 0, 0, 0, 0] or fingers == [1, 0, 0, 0, 0]:
        index_up = 0
    index_up = index_up + 1

    if fingers == [1, 1, 1, 1, 1] or fingers == [0, 1, 1, 1, 1]:
        index_down = 0
    index_down = index_down + 1



    # 显示鼠标操作
    if var_flag1.get() == '1':
        if flag_click == 1:
            cv2.putText(img, "Click", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        if info[4] > 0:
            cv2.putText(img, "Click", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            info[4] = info[4] - 1
        if info[0] > 0:
            cv2.putText(img, "Double Click", (10, 55), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            info[0] = info[0] - 1
        if info[1] > 0:
            cv2.putText(img, "Right Click", (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            info[1] = info[1] - 1
        if info[2] > 0:
            cv2.putText(img, "UP", (10, 95), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            info[2] = info[2] - 1
        if info[3] > 0:
            cv2.putText(img, "DOWN", (10, 129), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            info[3] = info[3] - 1
    
    
    
    # 显示图像在ARmouse窗口中
    if var_flag2.get() == '1':
        cv2.imshow("ARmouse", img)   
    
    
    
    cv2.waitKey(1)



    # 按L键退出程序
    if listener.is_pressed('L'):
        sys.exit()
