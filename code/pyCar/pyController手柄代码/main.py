'''
实验名称：pyCar蓝牙遥控车（pyController代码）
版本：v1.0
日期：2022.4
作者：01Studio
说明：pyController做蓝牙主机，pyCar做从机，手柄搜索到'pyCar'后发起连接，然后控制。
'''

#导入BLE主机模块
import ble_simple_central

while True:
    
    #执行主机扫描连接代码
    ble_simple_central.ble_connect()