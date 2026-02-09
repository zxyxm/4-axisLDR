import time
import datetime
from zmotion import ZMCWrapper


def main():
################################功能使用######################################################    
    #实例化运动卡
    zaux = ZMCWrapper()
    # 连接控制器ip   默认192.168.0.11
    # zaux.connect("192.168.0.21")
    zaux.connect("192.168.0.11")
    #打印回传的句柄
    print(zaux.handle)


    #设置轴号，eci2600只有六个轴
    axis_num0 =0#对应连续体0轴
    axis_num1 =1#对应连续体1轴
    axis_num2 =2#对应连续体2轴
    axis_num3 =3#对应连续体3轴
    axis_num4 =4#备用轴
    axis_num5 =5#备用轴


    #设置默认的速度和脉冲当量
    uints=3200/1    # 将脉冲当量设置为驱动器的细分时，运动位置就是圈数
    v=0.5

    #设置轴参数
    zaux.axis_setting(axis_num0 , 7, uints,v)
    zaux.axis_setting(axis_num1 , 7, uints,v)
    zaux.axis_setting(axis_num2 , 7, uints,v)
    zaux.axis_setting(axis_num3 , 7, uints,v)
    zaux.axis_setting(axis_num4 , 7, uints,v)
    zaux.axis_setting(axis_num5 , 7, uints,v)

    #运动测试

    # zaux.ZAux_Direct_Single_Vmove(axis_num0,1)#连续运动，（轴号，方向）
    # zaux.ZAux_Direct_Single_Vmove(axis_num1,1)#连续运动，（轴号，方向）
    # zaux.ZAux_Direct_Single_Vmove(axis_num2,1)#连续运动，（轴号，方向）
    # zaux.ZAux_Direct_Single_Vmove(axis_num3,1)#连续运动，（轴号，方向）
    # zaux.ZAux_Direct_Single_Vmove(axis_num4,1)#连续运动，（轴号，方向）
    # zaux.ZAux_Direct_Single_Vmove(axis_num5,1)#连续运动，（轴号，方向）

    zaux.ZAux_Direct_Single_Move(axis_num0,3)#相对运动，（轴号，方向），1就是一次脉冲当量，也就是3200，正好一圈
    # zaux.ZAux_Direct_Single_Move(axis_num3,1)


####################################################
    # time.sleep(3)#等待运动运行结束3s
    # zaux.ZAux_Direct_Single_Cancel(axis_num0)
    # zaux.ZAux_Direct_Single_Cancel(axis_num1)
    # zaux.ZAux_Direct_Single_Cancel(axis_num2)
    # zaux.ZAux_Direct_Single_Cancel(axis_num3)
    # zaux.ZAux_Direct_Single_Cancel(axis_num4)
    # zaux.ZAux_Direct_Single_Cancel(axis_num5)



    print(zaux.disconnect())

    print("程序已停止。")

if __name__ == "__main__":
    main()