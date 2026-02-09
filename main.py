import time
import datetime
from zmotion import ZMCWrapper
from motion import Motion, MotionError
# import DY094Reader


def main():
################################功能使用######################################################    
    #实例化运动卡
    motion = Motion("192.168.0.11")
    # 连接控制器ip   默认192.168.0.11
    # motion.connect("192.168.0.21")
    motion.openEth()
    #打印回传的句柄
    print(motion)


    #设置轴号，eci2600只有六个轴
    axis_num0 =0#对应连续体0轴
    axis_num1 =1#对应连续体1轴
    axis_num2 =2#对应连续体2轴
    axis_num3 =3#对应连续体3轴
    axis_num4 =4#备用轴
    axis_num5 =5#备用轴


    #设置默认的速度和脉冲当量
    uints=3200/1    # 将脉冲当量设置为驱动器的细分时，运动位置就是圈数
    v=3

    #设置轴参数
    motion.set_axis(axis_num0 , 7, v,uints)
    motion.set_axis(axis_num1 , 7, v,uints)
    motion.set_axis(axis_num2 , 7, v,uints)
    motion.set_axis(axis_num3 , 7, v,uints)
    motion.set_axis(axis_num4 , 7, v,uints)
    motion.set_axis(axis_num5 , 7, v,uints)

    #全部反转io信号
    motion.zmc.ZAux_Direct_SetInvertIn(motion.x0[2], 1)#0号轴远点，上限位
    motion.zmc.ZAux_Direct_SetInvertIn(motion.x0[0], 1)#0号轴零点
    motion.zmc.ZAux_Direct_SetInvertIn(motion.x0[1], 1)#0号轴近点，下限位


    motion.zmc.ZAux_Direct_SetInvertIn(motion.x1[2], 1)#1号轴远点，上限位
    motion.zmc.ZAux_Direct_SetInvertIn(motion.x1[0], 1)#1号轴零点
    motion.zmc.ZAux_Direct_SetInvertIn(motion.x1[1], 1)#1号轴近点，下限位

    motion.zmc.ZAux_Direct_SetInvertIn(motion.x2[2], 1)#2号轴远点，上限位
    motion.zmc.ZAux_Direct_SetInvertIn(motion.x2[0], 1)#2号轴零点
    motion.zmc.ZAux_Direct_SetInvertIn(motion.x2[1], 1)#2号轴近点，下限位

    motion.zmc.ZAux_Direct_SetInvertIn(motion.x3[2], 1)#3号轴远点，上限位
    motion.zmc.ZAux_Direct_SetInvertIn(motion.x3[0], 1)#3号轴零点
    motion.zmc.ZAux_Direct_SetInvertIn(motion.x3[1], 1)#3号轴近点，下限位

    # 开机全部解除拉力到上限位
    motion.go_switch(axis_num0,-1,motion.x0[2])#轴0向上负方向运动到x02光电
    # motion.go_switch(axis_num1,-1,motion.x1[2])
    motion.zmc.ZAux_Direct_Single_Move(axis_num1,-3)
    motion.go_switch(axis_num2,-1,motion.x2[2])
    motion.go_switch(axis_num3,-1,motion.x3[2])
    #设置io和归零
    # motion.ZAux_Direct_SetCreep(axis_num0,0.25)
    # 设置零点
    motion.set_home(axis_num0,motion.x0[0])
    motion.set_home(axis_num1,motion.x1[0])
    motion.set_home(axis_num2,motion.x2[0])
    motion.set_home(axis_num3,motion.x3[0])



    motion.home(axis_num0,wait=False)
    motion.home(axis_num1,wait=False)
    motion.home(axis_num2,wait=False)
    motion.home(axis_num3,wait=False)
    
    motion.wait_idle(axis_num0)
    motion.wait_idle(axis_num1)
    motion.wait_idle(axis_num2)
    motion.wait_idle(axis_num3)


    print("全部回零完毕")
    
    #重新设置运动速度
    v2=1

    #重新设置轴参数
    motion.set_axis(axis_num0 , 7, v2,uints)
    motion.set_axis(axis_num1 , 7, v2,uints)
    motion.set_axis(axis_num2 , 7, v2,uints)
    motion.set_axis(axis_num3 , 7, v2,uints)
    motion.set_axis(axis_num4 , 7, v2,uints)
    motion.set_axis(axis_num5 , 7, v2,uints)
    # 运动测试
    x=5
    motion.zmc.ZAux_Direct_Single_Move(axis_num0,x)
    # motion.zmc.ZAux_Direct_Single_Move(axis_num1,3)
    motion.zmc.ZAux_Direct_Single_Move(axis_num2,-x)
    # motion.zmc.ZAux_Direct_Single_Move(axis_num4,-3)



    # 关机向上运动，解除拉力
    # print("关机向上运动，解除拉力")
    # motion.zmc.ZAux_Direct_Single_Move(axis_num0,-3)
    # motion.zmc.ZAux_Direct_Single_Move(axis_num1,-3)
    # motion.zmc.ZAux_Direct_Single_Move(axis_num2,-3)
    # motion.zmc.ZAux_Direct_Single_Move(axis_num3,-3)


####################################################
    # time.sleep(3)#等待运动运行结束3s
    # motion.ZAux_Direct_Single_Cancel(axis_num0)
    # motion.ZAux_Direct_Single_Cancel(axis_num1)
    # motion.ZAux_Direct_Single_Cancel(axis_num2)
    # motion.ZAux_Direct_Single_Cancel(axis_num3)
    # motion.ZAux_Direct_Single_Cancel(axis_num4)
    # motion.ZAux_Direct_Single_Cancel(axis_num5)



    print(motion.close())

    print("程序已停止。")

if __name__ == "__main__":
    main()