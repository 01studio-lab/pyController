# pyController
由01Studio发起的MicroPython开源遥控/游戏手柄。  
![pyController](https://www.01studio.cc/data/picture/pyController.jpg)

## 项目简介
Micropython是指使用python做各类嵌入式硬件设备编程。MicroPython发展势头强劲，01Studio一直致力于Python嵌入式编程，特此推出pyController开源项目，旨在让MicroPython变得更加流行。使用MicroPython，你可以轻松地实现手柄控制、NES游戏、蓝牙WiFi遥控等功能。

例：
```python
#构建手柄对象
from controller import CONTROLLER
gamepad = CONTROLLER()

#使用方法
gamepad.read() #读取手柄按键摇杆数据

#构建nes游戏对象
from game import NES
nes = NES()

#使用方法
nes.start('/mario.nes') #运行flash里面的马里奥游戏
...
```

## 硬件资源
● 主控：ESP32-S3-WROOM-1 （N8R2; Flash:4MBytes,RAM:2MBytes）支持WiFi/BLE  
● 1 x LED 
● 11 x 按键（1个复位键+10个功能键）  
● 2 x 摇杆（360度带确认键）  
● 1 x 1.54寸显示屏（240x240）  
● 1 x UART/I2C接口（XH-1.25MM-4P）  
● 1 x 锂电池（3.7V 1200mAh），板载充电电路
● 1 x TPYE-C（下载/REPL调试/供电）  
● 1 x 拨码开关   


## 贡献说明
本项目预设以下文件夹：

### code
示例代码。

### docs
pyCar官方说明文档、MicroPython库文档。
https://pycontroller.01studio.cc/zh_CN/latest/manual/quickref.html

### firmware
pyController的MicroPython固件。
https://github.com/01studio-lab/micropython/tree/master/ports/esp32/boards/PYCONTROLLER

### hardware
硬件资料，原理图、尺寸图等。

### update.md
更新日志。

## 贡献用户
【CaptainJacky】 pyController项目发起人，负责硬件和MicroPython软件设计。    
【Spring641】pyController MicroPython底层开发。    

欢迎参与项目贡献！

## 联系方式
jackey@01studio.cc