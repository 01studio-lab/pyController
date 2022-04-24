# The MIT License (MIT)
#
# Copyright (c) 2021 , 01Studio

from machine import Pin,PWM,SoftI2C
from ssd1306 import SSD1306_I2C     #从ssd1306模块中导入SSD1306_I2C子模块
import framebuf
import time

#编码盘计数
count1 = 0
count2 = 0

class CAR():
    
    #初始化
    def __init__(self):
        
        #电机1
        self.M1_P = PWM(Pin(14), freq=1000, duty=0) 
        self.M1_N = PWM(Pin(15), freq=1000, duty=0)
        
        #电机2
        self.M2_P = PWM(Pin(16), freq=1000, duty=0) 
        self.M2_N = PWM(Pin(17), freq=1000, duty=0)
        
        #电机3
        self.M3_P = PWM(Pin(18), freq=1000, duty=0) 
        self.M3_N = PWM(Pin(19), freq=1000, duty=0)

        #电机4
        self.M4_P = PWM(Pin(21), freq=1000, duty=0) 
        self.M4_N = PWM(Pin(22), freq=1000, duty=0)

        #电机速度，默认最大
        self.duty=1023
        
        #车灯      
        self.light = Pin(5, Pin.OUT)

        #超声波测距
        self.trig = Pin(27,Pin.OUT)
        self.echo = Pin(26,Pin.IN)
        
        #编码盘测速
        self.speed = Pin(4,Pin.IN,Pin.PULL_UP)
        self.speed.irq(self.speed_count,Pin.IRQ_FALLING)
        self.speed2 = Pin(13,Pin.IN,Pin.PULL_UP)
        self.speed2.irq(self.speed_count2,Pin.IRQ_FALLING)
        
        #巡线传感器初始化，五路光电
        self.t1 = Pin(33, Pin.IN, Pin.PULL_UP)
        self.t2 = Pin(34, Pin.IN, Pin.PULL_UP)
        self.t3 = Pin(35, Pin.IN, Pin.PULL_UP)
        self.t4 = Pin(36, Pin.IN, Pin.PULL_UP)
        self.t5 = Pin(39, Pin.IN, Pin.PULL_UP)
        
        #红外接收头
        self.IR = Pin(32, Pin.IN)
        
        #屏幕
        self.i2c=SoftI2C(sda=Pin(25), scl=Pin(23))
        self.oled=SSD1306_I2C(128, 64,self.i2c,addr=0x3c)
        buf01studio=framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00g\xf1\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xfc\x1f\xe0\x1f\x03\x80|\x00\x00\x00\x19\x80\x00\x00\x00\x01\xf8\x07\xc0?\x87\x81\xff\x18\x00\x00\x19\xc0\x00\x00\x00\x00\xe0\x03\x809\xc7\x81\xc7\x18\x00\x00\x18\x00\x00\x00\x00\x00\xe1\xc1\xc0p\xc5\x83\x80\x18\x00\x00\x18\x00\x00\x00\x00\x00\xc1\xc0\xc0p\xc1\x83\x80<@\x81\x98\x81\x80\x00\x00\x03\xc0\xc0\xe0p\xc1\x83\x80>a\x87\xf9\xc7\xe0\x00\x00\x07\x80\xc0\xf8p\xc1\x81\xe0\x18a\x87\xf9\x8f\xf0\x00\x00\x07\x80\xc0\xf8p\xc1\x80\xfe\x18a\x8e9\x8e8\x00\x00\x07\x80\xc0\xf8p\xc1\x80\x7f\x18a\x8c\x19\x8c8\x00\x00\x07\x80\xc0\xf8p\xc1\x80\x07\x18a\x8c\x19\x8c8\x00\x00\x01\xc0\xc0\xc0p\xc1\x80\x03\x98a\x8c\x19\x8c\x18\x00\x00\x00\xc0\xc1\xc0p\xc1\x80\x03\x98a\x8c\x19\x8c8\x00\x00\x00\xe0\x01\x801\xc1\x83\x03\x18a\x8e9\x8e8\x00\x00\x00\xf0\x03\xc0?\xc1\x83\xff\x1c\x7f\x8f\xf9\x8f\xf0\x00\x00\x01\xf8\x0f\xc0\x1f\x81\xc1\xfe\x1e?\xc7\xf9\xc7\xe0\x00\x00\x01\xff\x7f\xc0\x0e\x01\x808\x04\x18\x81\x90\x81\x80\x00\x00\x00\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00C\xf1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xbc\x18\x18~\x07\xe0\xc6\x00\x00\x00\x00\x00\x00\x00\x00\x01\xff\x180\xff\x0f\xf0\xde\x00\x00\x00\x00\x00\x00\x00\x00\x01\xc3\x0c1\xc3\x0c0\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x01\x83\x0c1\x83\x000\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x01\x83\x8ca\x80\x03\xf0\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x01\x81\x86a\x80\x0f\xb0\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x01\x83\x86A\x81\x9c0\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x01\x83\x03\xc1\x83\x980\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x01\xc7\x03\xc0\xc3\x18p\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x01\xfe\x03\x80~\x0f\xf0\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x01\x9c\x01\x80<\x07\x18\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x01\x80\x01\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x80\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x80\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),128,64,framebuf.MONO_HLSB)
        self.oled.blit(buf01studio,0,0)
        self.oled.show()
        time.sleep(2)
        self.s_wifi=0
        self.s_blue=0
        self.s_red=0
        self.s_light=0
        self.s_forward=0
        self.s_backward=0
        self.s_left=0
        self.s_right=0
        self.s_sr=0
        self.s_distance=0
        self.screen()

    #屏幕刷新    
    def screen(self):
        if self.i2c.scan()[0]==0x3c:
            self.oled.fill(0)
            wifibuf=framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\x00\x10\x08\x14(\x14(\x14(\x10\x08\x00\x00\x01\x80\x01\x80\x01\x80\x01\xc0\x03\xc0\x00\x00\x00\x00\x00\x00'),16,16,framebuf.MONO_HLSB)
            bluetoothbuf=framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\x00\x01\x80\x01\xc0\x05`\x07\xc0\x03\x80\x01\x80\x03\xc0\x05`\x01\xc0\x01\x80\x00\x00\x00\x00\x00\x00\x00\x00'),16,16,framebuf.MONO_HLSB)
            redbuf=framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x01\x80\x19\x98\t\x90\x05\xa0\x04 \x00\x00\x03\xc0\x07\xe0\x1f\xf8\x00\x00\x00\x00\x00\x00'),16,16,framebuf.MONO_HLSB)
            lightbuf=framebuf.FrameBuffer(bytearray(b'\x00\x00\x03\x80\x0c`\x080\x10\x10\x10\x10\x11\x10\x19\x10\t \x05`\x07\xc0\x04@\x04@\x07\xc0\x03\x80\x00\x00'),16,16,framebuf.MONO_HLSB)
            arrowbuf=framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xc0\x00\x00\x00\x00\x00\x00\x03\xe0\x00\x00\x00\x00\x00\x00\x07\xf0\x00\x00\x00\x00\x00\x00\x0f\xf8\x00\x00\x00\x00\x00\x00\x0f\xf8\x00\x00\x00\x00\x00\x00\x1e<\x00\x00\x00\x00\x00\x00<\x1e\x00\x00\x00\x00\x00\x00x\x0f\x00\x00\x00\x00\x00\x00x\x0f\x00\x00\x00\x00\x00\x00\xf0\x07\x80\x00\x00\x00\x00\x01\xe0\x03\xc0\x00\x00\x00\x00\x01\xe0\x03\xc0\x00\x00\x00\x00\x01\xfc\x1f\xc0\x00\x00\x00\x00\x01\xfc\x1f\xc0\x00\x00\x00\x00\x00\xfc\x1f\x80\x00\x00\x00\x00\x00\x1c\x1c\x00\x00\x00\x00\x00\x00\x1c\x1c\x00\x00\x00\x00\x00\x00\x1c\x1c\x00\x00\x00\x00\x00\x00\x1c\x1c\x00\x00\x00\x00\x00\x00\x1c\x1c\x00\x00\x00\x00\x00\x00\x1c\x1c\x00\x00\x00\x00\x0f\x00\x1c\x1c\x00x\x00\x00\x1f\x80\x1c\x1c\x00\xfc\x00\x00\x7f\x80\x1c\x1c\x00\xff\x00\x00\xff\x80\x1c\x1c\x00\xff\x80\x01\xf3\xff\xff\xff\xff\xe7\xc0\x07\xe3\xff\xff\xff\xff\xe3\xf0\x0f\x83\xff\xff\xff\xff\xe0\xf8\x1f\x00\x00\x1f\xfc\x00\x00|>\x00\x00\x1f\xfc\x00\x00>>\x00\x00\x1f\xfc\x00\x00>>\x00\x00\x1f\xfc\x00\x00>\x1f\x00\x00\x1f\xfc\x00\x00|\x0f\x83\xff\xff\xff\xff\xe0\xf8\x07\xe3\xff\xff\xff\xff\xe3\xf0\x01\xf3\xff\xff\xff\xff\xe7\xc0\x00\xff\x80\x1c\x1c\x00\xff\x80\x00\x7f\x80\x1c\x1c\x00\xff\x00\x00\x1f\x80\x1c\x1c\x00\xfc\x00\x00\x0f\x00\x1c\x1c\x00x\x00\x00\x00\x00\x1c\x1c\x00\x00\x00\x00\x00\x00\x1c\x1c\x00\x00\x00\x00\x00\x00\x1c\x1c\x00\x00\x00\x00\x00\x00\x1c\x1c\x00\x00\x00\x00\x00\x00\x1c\x1c\x00\x00\x00\x00\x00\x00\x1c\x1c\x00\x00\x00\x00\x00\x00\xfc\x1f\x80\x00\x00\x00\x00\x01\xfc\x1f\xc0\x00\x00\x00\x00\x01\xfc\x1f\xc0\x00\x00\x00\x00\x01\xe0\x03\xc0\x00\x00\x00\x00\x01\xe0\x03\xc0\x00\x00\x00\x00\x00\xf0\x07\x80\x00\x00\x00\x00\x00x\x0f\x00\x00\x00\x00\x00\x00x\x0f\x00\x00\x00\x00\x00\x00<\x1e\x00\x00\x00\x00\x00\x00\x1e<\x00\x00\x00\x00\x00\x00\x0f\xf8\x00\x00\x00\x00\x00\x00\x0f\xf8\x00\x00\x00\x00\x00\x00\x07\xf0\x00\x00\x00\x00\x00\x00\x03\xe0\x00\x00\x00\x00\x00\x00\x01\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),64,64,framebuf.MONO_HLSB)
            
            if self.s_wifi:
                self.oled.blit(wifibuf,0,1)
            if self.s_blue:
                self.oled.blit(bluetoothbuf,0,17)
            if self.s_red:
                self.oled.blit(redbuf,0,31)
            if self.s_light:
                self.oled.blit(lightbuf,1,47)
                
            self.oled.blit(arrowbuf,17,0)
            
            if self.s_forward:
                self.oled.fill_rect(49,27,26,11,1)
            if self.s_backward:
                self.oled.fill_rect(24,27,26,11,1)
            if self.s_left:
                self.oled.fill_rect(44,7,11,26,1)
            if self.s_right:
                self.oled.fill_rect(44,32,11,26,1)
            
            self.oled.text("D:cm", 84,8)
            self.oled.text("%.2f" % self.s_distance,84,18)
            self.oled.text("G:cm",84,38)   
            self.oled.text("%.2f" % self.s_sr,84,48)      
            self.oled.vline(16,0,64,1)
            self.oled.vline(82,0,64,1)
            self.oled.hline(82,32,40,1)
            self.oled.rect(0,0,128,64,1)

            self.oled.show()
        else:
            print('screen connect error!')
        
    #调速
    def setspeed(self,speed):
        self.duty=speed
        if self.s_forward==1:
            self.forward()
        if self.s_backward==1:
            self.backward()
        if self.s_left==1:
            self.turn_left()
        if self.s_right==1:
            self.turn_right()
    #前进    
    def forward(self):
        speed=self.duty
        self.s_forward=1
        self.s_backward=0
        self.s_left=0
        self.s_right=0
        
        self.M1_P.duty(speed)
        self.M1_N.duty(0)    
        self.M2_P.duty(speed)
        self.M2_N.duty(0)
        self.M3_P.duty(speed)
        self.M3_N.duty(0)
        self.M4_P.duty(speed)
        self.M4_N.duty(0)
    
    #后退
    def backward(self):
        speed=self.duty
        self.s_forward=0
        self.s_backward=1
        self.s_left=0
        self.s_right=0

        self.M1_P.duty(0)
        self.M1_N.duty(speed)    
        self.M2_P.duty(0)
        self.M2_N.duty(speed)
        self.M3_P.duty(0)
        self.M3_N.duty(speed)
        self.M4_P.duty(0)
        self.M4_N.duty(speed)

    #左转
    def turn_left(self, mode=0):
        speed=self.duty
        self.s_forward=0
        self.s_backward=0
        self.s_left=1
        self.s_right=0
        
        #普通转向
        if mode == 0: 
            self.M1_P.duty(0)
            self.M1_N.duty(0)    
            self.M2_P.duty(speed)
            self.M2_N.duty(0)
            self.M3_P.duty(speed)
            self.M3_N.duty(0)
            self.M4_P.duty(0)
            self.M4_N.duty(0)
        
        #大幅度转向
        elif mode ==1:
            self.M1_P.duty(0)
            self.M1_N.duty(speed)    
            self.M2_P.duty(speed)
            self.M2_N.duty(0)
            self.M3_P.duty(speed)
            self.M3_N.duty(0)
            self.M4_P.duty(0)
            self.M4_N.duty(speed)

    #右转
    def turn_right(self, mode=0):
        speed=self.duty
        self.s_forward=0
        self.s_backward=0
        self.s_left=0
        self.s_right=1
        #普通转向
        if mode == 0:
            self.M1_P.duty(speed)
            self.M1_N.duty(0)    
            self.M2_P.duty(0)
            self.M2_N.duty(0)
            self.M3_P.duty(0)
            self.M3_N.duty(0)
            self.M4_P.duty(speed)
            self.M4_N.duty(0)
        #大幅度转向
        elif mode == 1: 
            self.M1_P.duty(speed)
            self.M1_N.duty(0)    
            self.M2_P.duty(0)
            self.M2_N.duty(speed)
            self.M3_P.duty(0)
            self.M3_N.duty(speed)
            self.M4_P.duty(speed)
            self.M4_N.duty(0)

    #停止
    def stop(self):
        self.s_forward=0
        self.s_backward=0
        self.s_left=0
        self.s_right=0
        self.M1_P.duty(0)
        self.M1_N.duty(0)    
        self.M2_P.duty(0)
        self.M2_N.duty(0)
        self.M3_P.duty(0)
        self.M3_N.duty(0)
        self.M4_P.duty(0)
        self.M4_N.duty(0)

    #####################
    # Mecanum麦克纳母轮
    #####################   
    def up(self): #上移
        
        speed=self.duty        
        self.M1_P.duty(speed)
        self.M1_N.duty(0)    
        self.M2_P.duty(speed)
        self.M2_N.duty(0)
        self.M3_P.duty(speed)
        self.M3_N.duty(0)
        self.M4_P.duty(speed)
        self.M4_N.duty(0)
        
    def down(self): #下移
        
        speed=self.duty 
        self.M1_P.duty(0)
        self.M1_N.duty(speed)    
        self.M2_P.duty(0)
        self.M2_N.duty(speed)
        self.M3_P.duty(0)
        self.M3_N.duty(speed)
        self.M4_P.duty(0)
        self.M4_N.duty(speed)

    def left(self): #左移
        
        speed=self.duty 
        self.M1_P.duty(0)
        self.M1_N.duty(speed)    
        self.M2_P.duty(speed)
        self.M2_N.duty(0)
        self.M3_P.duty(0)
        self.M3_N.duty(speed)
        self.M4_P.duty(speed)
        self.M4_N.duty(0)

    def right(self): #右移
        
        speed=self.duty 
        self.M1_P.duty(speed)
        self.M1_N.duty(0)    
        self.M2_P.duty(0)
        self.M2_N.duty(speed)
        self.M3_P.duty(speed)
        self.M3_N.duty(0)
        self.M4_P.duty(0)
        self.M4_N.duty(speed)

    def up_left(self): #左前移
        
        speed=self.duty 
        self.M1_P.duty(0)
        self.M1_N.duty(0)    
        self.M2_P.duty(speed)
        self.M2_N.duty(0)
        self.M3_P.duty(0)
        self.M3_N.duty(0)
        self.M4_P.duty(speed)
        self.M4_N.duty(0)

    def up_right(self): #右前移
        
        speed=self.duty 
        self.M1_P.duty(speed)
        self.M1_N.duty(0)    
        self.M2_P.duty(0)
        self.M2_N.duty(0)
        self.M3_P.duty(speed)
        self.M3_N.duty(0)
        self.M4_P.duty(0)
        self.M4_N.duty(0)

    def down_left(self): #左后移
        
        speed=self.duty 
        self.M1_P.duty(0)
        self.M1_N.duty(speed)    
        self.M2_P.duty(0)
        self.M2_N.duty(0)
        self.M3_P.duty(0)
        self.M3_N.duty(speed)
        self.M4_P.duty(0)
        self.M4_N.duty(0)
    
    def down_right(self): #右后移
        
        speed=self.duty 
        self.M1_P.duty(0)
        self.M1_N.duty(0)    
        self.M2_P.duty(0)
        self.M2_N.duty(speed)
        self.M3_P.duty(0)
        self.M3_N.duty(0)
        self.M4_P.duty(0)
        self.M4_N.duty(speed)

    def clockwise(self): #顺时针旋转
        
        speed=self.duty 
        self.M1_P.duty(speed)
        self.M1_N.duty(0)    
        self.M2_P.duty(0)
        self.M2_N.duty(speed)
        self.M3_P.duty(0)
        self.M3_N.duty(speed)
        self.M4_P.duty(speed)
        self.M4_N.duty(0)

    def Counterclockwise(self): #逆时针旋转
        
        speed=self.duty 
        self.M1_P.duty(0)
        self.M1_N.duty(speed)    
        self.M2_P.duty(speed)
        self.M2_N.duty(0)
        self.M3_P.duty(speed)
        self.M3_N.duty(0)
        self.M4_P.duty(0)
        self.M4_N.duty(speed)
    

    #打开车头灯
    def light_on(self):
        
        self.light.on()
        self.s_light=1
    
    #关闭车头灯
    def light_off(self):
        
        self.light.off()
        self.s_light=0
    
    #车头灯引脚输出
    def light(self,value):
        
        if value == 0:
            self.light.off()
        elif value == 1:
            self.light.on()

    #超声波测距
    def getDistance(self):
        distance=0
        self.trig.value(1)
        time.sleep_us(20)
        self.trig.value(0)
        while self.echo.value() == 0:
            pass
        if self.echo.value() == 1:
            ts=time.ticks_us()            #开始时间
            while self.echo.value() == 1: #等待脉冲高电平结束
                pass
            te=time.ticks_us()            #结束时间
            tc=te-ts                      #回响时间（单位us，1us=1*10^(-6)s）
            distance=(tc*170)/10000       #距离计算 （单位为:cm）
        self.s_sr=distance
            
        return distance

    #编码盘测速计数(1为左，2为右)
    def speed_count(self,args):
        
        global count1
        count1 = count1+1
        
    def speed_count2(self,args):
        
        global count2
        count2 = count2+1

    #返回行驶路程 
    def getJourney(self):     
        
        global count1
        global count2
        self.s_distance=count1/20*0.188
        return '%.2f'%(count1/20*0.188),'%.2f'%(count2/20*0.188)
    
    #路程清0
    def journey_clear(self):       
        
        global count1
        global count2
        count1 = 0
        count2 = 0

    #五路光电传感器
    def T1(self):
        
        return self.t1.value()

    def T2(self):
        
        return self.t2.value()
    
    def T3(self):
        
        return self.t3.value()

    def T4(self):
        
        return self.t4.value()
    
    def T5(self):
        
        return self.t5.value()

    #红外接收解码
    def getIR(self):

        if (self.IR.value() == 0):
            count = 0
            while ((self.IR.value() == 0) and (count < 100)): #9ms
                count += 1
                time.sleep_us(100)
            if(count < 10):
                return None
            count = 0
            while ((self.IR.value() == 1) and (count < 50)): #4.5ms
                count += 1
                time.sleep_us(100)
                
            idx = 0
            cnt = 0
            data = [0,0,0,0]
            for i in range(0,32):
                count = 0
                while ((self.IR.value() == 0) and (count < 10)):    #0.56ms
                    count += 1
                    time.sleep_us(100)

                count = 0
                while ((self.IR.value() == 1) and (count < 20)):   #0: 0.56mx
                    count += 1                                #1: 1.69ms
                    time.sleep_us(100)

                if count > 7:
                    data[idx] |= 1<<cnt
                if cnt == 7:
                    cnt = 0
                    idx += 1
                else:
                    cnt += 1

            if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:  #check
                return data[2]
            else:
                return("REPEAT")

