'''
实验名称：网络时钟
版本：v1.0
日期：2022.4
作者：01Studio
实验平台：pyController遥控手柄
说明:在线获取实时时间，然后通过LCD表盘显示
'''

#导入相关模块
from tftlcd import LCD15
from machine import RTC,Pin
import time,math,ntptime,network

#WiFi账号密码，修改成自己的。
SSID='01Studio' # wiFi账号
KEY='88888888'  # WiFi密码

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

########################
# 构建1.5寸LCD对象并初始化
########################
d = LCD15(portrait=1) #默认方向竖屏

#填充白色
d.fill(BLACK)

#WIFI连接函数,连接成功后更新时间
def WIFI_Connect():

    WIFI_LED=Pin(46, Pin.OUT) #初始化WIFI指示灯
    
    wlan = network.WLAN(network.STA_IF) #STA模式
    wlan.active(True)                   #激活接口
    start_time=time.time()              #记录时间做超时判断

    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, KEY) #WIFI账号密码连接

        while not wlan.isconnected():

            #LED闪烁提示
            WIFI_LED.value(1)
            time.sleep_ms(300)
            WIFI_LED.value(0)
            time.sleep_ms(300)
            
            #超时判断,15秒没连接成功判定为超时
            if time.time()-start_time > 15 :
                print('WIFI Connected Timeout!')
                break

    if wlan.isconnected():

        #串口打印信息
        print('network information:', wlan.ifconfig())

        for i in range(5): #最多尝试获取5次时间
            try:
                ntptime.settime() #获取的是伦敦时间
                print("ntp time: ",rtc.datetime())
                time.sleep_ms(500)
                return None

            except:
                print("Can not get time!")

#画圆
d.drawCircle(120, 120, 100, BLUE, border=5)
for i in range(12):
    
    x0 = 120+round(95*math.sin(math.radians(i*30)))
    y0 = 120-round(95*math.cos(math.radians(i*30)))
    x1 = 120+round(85*math.sin(math.radians(i*30)))
    y1 = 120-round(85*math.cos(math.radians(i*30)))
    d.drawLine(x0, y0, x1, y1, WHITE)

rtc = RTC() #构建RTC时钟对象

#连接WiFi并获取时间
WIFI_Connect()

while True:   
    
    datetime = rtc.datetime() #获取当前时间
    second = datetime[6]
    minute = datetime[5]
    hour = (datetime[4]+8)%12 #北京时间是东八区，+8
    
    #秒钟处理
    
    #清除上一帧
    x0 = 120+round(80*math.sin(math.radians(second*6-6)))
    y0 = 120-round(80*math.cos(math.radians(second*6-6)))
    d.drawLine(x0, y0, 120, 120, BLACK)
    
    #显示
    x1 = 120+round(80*math.sin(math.radians(second*6)))
    y1 = 120-round(80*math.cos(math.radians(second*6)))
    d.drawLine(x1, y1, 120, 120, WHITE)
    
    #分钟处理
    
    #清除上一帧
    x0 = 120+round(65*math.sin(math.radians(minute*6-6)))
    y0 = 120-round(65*math.cos(math.radians(minute*6-6)))
    d.drawLine(x0, y0, 120, 120, BLACK)
    
    #显示
    x1 = 120+round(65*math.sin(math.radians(minute*6)))
    y1 = 120-round(65*math.cos(math.radians(minute*6)))
    d.drawLine(x1, y1, 120, 120, GREEN)
        
    #时钟处理

    #清除上一帧
    x0 = 120+round(55*math.sin(math.radians(hour*30+int(minute/12)*6-6)))
    y0 = 120-round(55*math.cos(math.radians(hour*30+int(minute/12)*6-6)))
    d.drawLine(x0, y0, 120, 120, BLACK)
    
    #显示
    x1 = 120+round(55*math.sin(math.radians(hour*30+int(minute/12)*6)))
    y1 = 120-round(55*math.cos(math.radians(hour*30+int(minute/12)*6)))
    d.drawLine(x1, y1, 120, 120, RED)
    
    time.sleep_ms(200) #显示间隔200ms