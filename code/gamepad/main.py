'''
实验名称：手柄控制
版本：v1.0
日期：2022.4
作者：01Studio
说明：通过获取手柄动作信息在LCD显示
'''

import controller,time
from tftlcd import LCD15

#构建手柄对象
gamepad = controller.CONTROLLER()

########################
# 构建1.5寸LCD对象并初始化
########################
d = LCD15(portrait=1) #默认方向竖屏

#常用颜色定义
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)

d.fill(WHITE) #填充白色

#相关图形显示，用于展示动作
d.drawCircle(60,115,15,color=BLACK,border=2,fillcolor=WHITE)
d.drawCircle(60,175,15,color=BLACK,border=2,fillcolor=WHITE)
d.drawCircle(30,145,15,color=BLACK,border=2,fillcolor=WHITE)
d.drawCircle(90,145,15,color=BLACK,border=2,fillcolor=WHITE)

d.drawCircle(180,20,15,color=BLACK,border=2,fillcolor=WHITE)
d.drawCircle(180,80,15,color=BLACK,border=2,fillcolor=WHITE)
d.drawCircle(150,50,15,color=BLACK,border=2,fillcolor=WHITE)
d.drawCircle(210,50,15,color=BLACK,border=2,fillcolor=WHITE)

d.drawCircle(30,85,10,color=BLACK,border=2,fillcolor=WHITE)
d.drawCircle(210,105,10,color=BLACK,border=2,fillcolor=WHITE)

d.drawRect(90, 90, 25, 15, color=BLACK, border=2, fillcolor=WHITE)
d.drawRect(125, 90, 25, 15, color=BLACK, border=2, fillcolor=WHITE)


while True:
    
    v = gamepad.read()
    
    print(v) #REPL打印
        
    #摇杆数据
    d.printStr('L-X: '+str(v[1])+'  ',10,15,color=BLACK,size=2)
    d.printStr('L-Y: '+str(v[2])+'  ',10,45,color=BLACK,size=2)
    
    d.printStr('R-X: '+str(v[3])+'  ',130,120,color=BLACK,size=2)
    d.printStr('R-Y: '+str(v[4])+'  ',130,150,color=BLACK,size=2)
    
    #按键动作判断并显示
    L = v[5]%16
    if L == 0: #上
        d.drawCircle(60,115,15,color=BLACK,border=2,fillcolor=BLACK)
        time.sleep_ms(200)
        d.drawCircle(60,115,15,color=BLACK,border=2,fillcolor=WHITE)

    if L == 4: #下
        d.drawCircle(60,175,15,color=BLACK,border=2,fillcolor=BLACK)
        time.sleep_ms(200)
        d.drawCircle(60,175,15,color=BLACK,border=2,fillcolor=WHITE)

    if L == 6: #左
        d.drawCircle(30,145,15,color=BLACK,border=2,fillcolor=BLACK)
        time.sleep_ms(200)
        d.drawCircle(30,145,15,color=BLACK,border=2,fillcolor=WHITE)
        
    if L == 2: #右
        d.drawCircle(90,145,15,color=BLACK,border=2,fillcolor=BLACK)
        time.sleep_ms(200)
        d.drawCircle(90,145,15,color=BLACK,border=2,fillcolor=WHITE)
    
    
    if v[5] & 1<<4: #Y
        d.drawCircle(180,20,15,color=BLACK,border=2,fillcolor=BLACK)
        time.sleep_ms(200)
        d.drawCircle(180,20,15,color=BLACK,border=2,fillcolor=WHITE)
    
    if v[5] & 1<<6: #A
        d.drawCircle(180,80,15,color=BLACK,border=2,fillcolor=BLACK)
        time.sleep_ms(200)
        d.drawCircle(180,80,15,color=BLACK,border=2,fillcolor=WHITE)
        
    if v[5] & 1<<7: #X
        d.drawCircle(150,50,15,color=BLACK,border=2,fillcolor=BLACK)
        time.sleep_ms(200)
        d.drawCircle(150,50,15,color=BLACK,border=2,fillcolor=WHITE)
    
    if v[5] & 1<<5: #B
        d.drawCircle(210,50,15,color=BLACK,border=2,fillcolor=BLACK)
        time.sleep_ms(200)
        d.drawCircle(210,50,15,color=BLACK,border=2,fillcolor=WHITE)
    
    if v[6] & 1<<4: #back
        d.drawRect(90, 90, 25, 15, color=BLACK, border=2, fillcolor=BLACK)
        time.sleep_ms(200)
        d.drawRect(90, 90, 25, 15, color=BLACK, border=2, fillcolor=WHITE)

    if v[6] & 1<<5: #start
        d.drawRect(125, 90, 25, 15, color=BLACK, border=2, fillcolor=BLACK)
        time.sleep_ms(200)
        d.drawRect(125, 90, 25, 15, color=BLACK, border=2, fillcolor=WHITE)
    
    if v[6] & 1<<6: #右摇杆确认键
        d.drawCircle(210,105,10,color=BLACK,border=2,fillcolor=BLACK)
        time.sleep_ms(200)
        d.drawCircle(210,105,10,color=BLACK,border=2,fillcolor=WHITE)

    if v[6] & 1<<7: #左摇杆确认键
        d.drawCircle(30,85,10,color=BLACK,border=2,fillcolor=BLACK)
        time.sleep_ms(200)
        d.drawCircle(30,85,10,color=BLACK,border=2,fillcolor=WHITE)
    
        
    time.sleep_ms(20) #20ms检测一次
