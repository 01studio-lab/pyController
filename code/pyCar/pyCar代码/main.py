'''
实验名称：pyCar蓝牙遥控车（pyCar代码）
版本：v1.0
日期：2022.4
作者：01Studio
说明：pyController做蓝牙主机，pyCar做从机，手柄搜索到'pyCar'后发起连接，然后控制。
'''

import bluetooth,ble_simple_peripheral,time
from car import CAR

#初始化pyCar
Car = CAR()
time.sleep_ms(300) #等待稳定

#初始化蓝牙BLE从机,广播名称为pyCar
ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble,name='pyCar')

#车灯状态
light_state = 0

#接收到蓝牙数据处理函数
def on_rx(v):

    global light_state
    
    #串口打印接收到的数据
    #print("RX:", v)
    
    #对收到的手柄8字节数据进行判断
    
    if v[5]==40: #B键被按下，开车灯
        Car.light(1)
        
    if v[5]==72: #A键被按下，关车灯
        Car.light(0)
        
    if v[5]==0: #上键被按下，前进
        Car.forward()
        
    if v[5]==4: #下键被按下，后退
        Car.backward() 
        
    if v[5]==6: #左键被按下，左转
        Car.turn_left(mode=1)
        
    if v[5]==2: #右键被按下，右转
        Car.turn_right(mode=1)
        
    if v[5]==8: #没按键按下，停止
        Car.stop()

#注册从机接收回调函数，收到数据会进入on_rx函数。
p.on_write(on_rx)

#系统会自动广播, 连接断开后重新自动广播。
while True:
    
    pass



