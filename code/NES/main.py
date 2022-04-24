'''
实验名称：NES游戏机
版本：v1.0
日期：2022.4
作者：01Studio
说明：运行NES游戏
'''

import game,tftlcd

d = tftlcd.LCD15(portrait=1) #LCD初始化

nes = game.NES() #构造NES对象

#启动游戏,启动后进入阻塞，无法中断。
nes.start('/nes/mario.nes') 
