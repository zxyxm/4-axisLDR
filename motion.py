import time
from zmotion import ZMCWrapper

class MotionError(RuntimeError): pass
class MotionTimeout(MotionError): pass

class Motion:
    def __init__(self, ip: str):
        self.ip = ip
        self.zmc = ZMCWrapper()#zmotion.py
        self._connected = False

        #设置io口变量
        self.x0=(1,2,0)#0号轴远点，上限位;零点;近点，下限位
        self.x1=(4,5,3)
        self.x2=(11,12,10)
        self.x3=(14,15,13)
     

    # ===== connection =====
    def openEth(self):
        if self._connected: return
        if self.zmc.ZAux_OpenEth(self.ip) != 0:
            raise MotionError(f"Connect failed to {self.ip}")
        self._connected = True
        print(f"Connected to {self.ip} successfully!")

    def close(self):
        if self._connected:
            self.zmc.ZAux_Close()
            self._connected = False
            print("Connection closed!")

    def _require_connected(self):
        if not self._connected:
            raise MotionError("Controller not connected")

    # ===== axis setup =====
    def set_axis(self, axis: int, 
                 atype=1, 
                 speed=100, 
                 units=100, 
                 accel=100, 
                 decel=100, 
                 sramp=1000):
        self._require_connected()
        # self.zmc.ZAux_Direct_SetDpos(axis, dpos)
        self.zmc.ZAux_Direct_SetAtype(axis, atype)
        self.zmc.ZAux_Direct_SetSpeed(axis, speed)
        self.zmc.ZAux_Direct_SetUnits(axis, units)
        self.zmc.ZAux_Direct_SetAccel(axis, accel)
        self.zmc.ZAux_Direct_SetDecel(axis, decel)
        self.zmc.ZAux_Direct_SetSramp(axis, sramp)
        print(f"Axis {axis} setup complete")

    def get_axis(self, axis: int):
        self._require_connected()
        _, atype = self.zmc.ZAux_Direct_GetAtype(axis)
        _, speed = self.zmc.ZAux_Direct_GetSpeed(axis)
        _, units = self.zmc.ZAux_Direct_GetUnits(axis)
        _, accel = self.zmc.ZAux_Direct_GetAccel(axis)
        _, decel = self.zmc.ZAux_Direct_GetDecel(axis)
        _, sramp = self.zmc.ZAux_Direct_GetSramp(axis)
        return atype, speed, units, accel, decel, sramp
    
    # ===== get position =====
    def get_pos(self, axis: int):
        self._require_connected()
        _, dpos = self.zmc.ZAux_Direct_GetDpos(axis)
        _, mpos = self.zmc.ZAux_Direct_GetMpos(axis)
        return dpos, mpos
    
    # ===== simple motion =====
    def move_rel(self, axis: int, 
                 distance: float, 
                 wait=True, timeout=10.0):
        self._require_connected()
        if self.zmc.ZAux_Direct_Single_Move(axis, distance) != 0:
            raise MotionError(f"MoveRel failed, axis={axis}")
        print(f"Axis {axis} moving {distance} units")
        if wait: self.wait_idle(axis, timeout)

    def move_abs(self, axis: int, 
                 pos: float, 
                 wait=True, timeout=10.0):
        self._require_connected()
        if self.zmc.ZAux_Direct_Single_MoveAbs(axis, pos) != 0:
            raise MotionError(f"MoveAbs failed, axis={axis}")
        print(f"Axis {axis} moving to {pos}")
        if wait: self.wait_idle(axis, timeout)

    def move_line_rel(self, axislist, distances, 
                      wait=True, timeout=10.0):
        self._require_connected()
        if len(axislist) != len(distances):
            raise MotionError("axislist/distances length mismatch")
        ret = self.zmc.ZAux_Direct_Move(
            len(axislist),
            axislist,
            [float(d) for d in distances]
        )
        if ret != 0:
            raise MotionError(f"MoveLineRel failed, ret={ret}")
        if wait:
            for ax in axislist:
                self.wait_idle(ax, timeout)

    def move_line_abs(self, axislist, positions, 
                      wait=True, timeout=10.0):
        self._require_connected()
        if len(axislist) != len(positions):
            raise MotionError("axislist/positions length mismatch")
        ret = self.zmc.ZAux_Direct_MoveAbs(
            len(axislist),
            axislist,
            [float(p) for p in positions]
        )
        if ret != 0:
            raise MotionError(f"MoveLineAbs failed, ret={ret}")
        if wait:
            for ax in axislist:
                self.wait_idle(ax, timeout)

    def move_circ2_rel(self, axislist, mid, end, 
                       wait=True, timeout=10.0):
        self._require_connected()
        if len(axislist) != 2:
            raise MotionError("Circ2 needs exactly 2 axes")
        ret = self.zmc.ZAux_Direct_MoveCirc2(
            2, axislist,
            float(mid[0]), float(mid[1]),
            float(end[0]), float(end[1])
        )
        if ret != 0:
            raise MotionError(f"MoveCirc2 failed, ret={ret}")
        if wait:
            for ax in axislist:
                self.wait_idle(ax, timeout)

    def move_spherical(self, axislist, center, end, 
                       wait=True, timeout=10.0):
        self._require_connected()
        if len(axislist) != 3:
            raise MotionError("MSpherical needs 3 axes")
        ret = self.zmc.ZAux_Direct_MSpherical(
            3, axislist,
            float(center[0]), float(center[1]), float(center[2]),
            float(end[0]), float(end[1]), float(end[2])
        )
        if ret != 0:
            raise MotionError(f"MSpherical failed, ret={ret}")
        if wait:
            for ax in axislist:
                self.wait_idle(ax, timeout)
    
    def move_helical_rel(self, axislist, end, center, distance3,
                     direction=0, mode=0,
                     wait=True, timeout=10.0):
        self._require_connected()
        if len(axislist) != 3:
            raise MotionError("MHelical needs exactly 3 axes")
        ret = self.zmc.ZAux_Direct_MHelical(
            3, axislist,
            float(end[0]), float(end[1]),
            float(center[0]), float(center[1]),
            int(direction),
            float(distance3),
            int(mode)
        )
        if ret != 0:
            raise MotionError(f"MHelical failed, ret={ret}")
        if wait:
            for ax in axislist:
                self.wait_idle(ax, timeout)

    # ===== wait / monitor =====
    def wait_idle(self, axis: int, 
                  timeout=10.0, poll=0.1):
        self._require_connected()
        start = time.time()
        while True:
            _, idle = self.zmc.ZAux_Direct_GetIfIdle(axis)
            if idle:
                print(f"Axis {axis} is idle")
                break
            _, dpos = self.zmc.ZAux_Direct_GetDpos(axis)
            _, mpos = self.zmc.ZAux_Direct_GetMpos(axis)
            print(f"Moving... DPOS={dpos:.2f}, MPOS={mpos:.2f}")
            if time.time() - start > timeout:
                raise MotionTimeout(f"Axis {axis} wait idle timeout")
            time.sleep(poll)

    # ===== homing =====
    """配置回零相关参数（ECI2600）a:[1, 3, 4] -> m:[3, 3, 4]  
    # home_in = 0 , mode = 4 for axis 0 #物理受限
    # home_in = 1 , mode = 3 for axis 0
    # home_in = 2 , mode = 4 for axis 1
    # home_in = 3 , mode = 3 for axis 1
    # home_in = 4 , mode = 4 for axis 2
    # home_in = 5 , mode = 3 for axis 2
    """
    """配置回零相关参数（ECI3808）a:[18, 22, 24] -> m:[3, 3, 4]  
    # home_in = 16 , mode = 4 for axis 0 #物理受限
    # home_in = 18 , mode = 3 for axis 0
    # home_in = 20 , mode = 4 for axis 1
    # home_in = 22 , mode = 3 for axis 1
    # home_in = 24 , mode = 4 for axis 2
    # home_in = 26 , mode = 3 for axis 2
    """
    def set_home(self, axis: int, 
                 home_io=1000, 
                 home_wait=100, 
                #  invert_level=1, 
                 creep_speed=None, 
                 fwd_limit_in=1000, 
                 rev_limit_in=1000):
       
        self._require_connected()
        # self.zmc.ZAux_Direct_SetDpos(axis, 1)
        self.zmc.ZAux_Direct_SetDatumIn(axis, home_io)
        self.zmc.ZAux_Direct_SetHomeWait(axis, home_wait)
        # self.zmc.ZAux_Direct_SetInvertIn(axis, invert_level)
        self.zmc.ZAux_Direct_SetFwdIn(axis, fwd_limit_in)
        self.zmc.ZAux_Direct_SetRevIn(axis, rev_limit_in)
        
        if creep_speed is not None:
            self.zmc.ZAux_Direct_SetCreep(axis, creep_speed)
        print(f"Home configuration set for axis {axis}")
        
    """执行回零"""
    def home(self, axis: int, mode=3, wait=True, timeout=15.0):
        #3正方向回零，4负方向回零
        self._require_connected()
        ret=self.zmc.ZAux_Direct_Single_Datum(axis, mode)
        if ret == 1:#正常为0
            raise MotionError(f"Homing failed, axis={axis}")
        if wait:
            self.wait_idle(axis, timeout)
            print(f"Homing finished on axis {axis}")


    
    # 到达某个光电开关
    def go_switch(self, axis: int, direction: int, io: int):
        self._require_connected()  # 检查设备连接状态
        # 1. 发送连续点动指令，让轴向指定方向运动（direction控制正/反，速度由控制器提前配置）
        self.zmc.ZAux_Direct_Single_Vmove(axis, direction)
        print(f"轴{axis}向{direction}方向运动，寻找光电开关IO{io}...")
        # 2. 循环检测IO信号，直到光电开关被触发（IO信号为0，常规光电开关是低电平触发）
        while self.zmc.ZAux_Direct_GetIn(io)[1] == 0:
            print(f"轴{axis}的光电开光IO{io}状态：{self.zmc.ZAux_Direct_GetIn(io)[1]} 运动中...")
            # 信号未触发时，空循环等待（也可加微小延时减少CPU占用，如time.sleep(0.01)）
            time.sleep(0.01)
            pass
        # 3. 光电开关触发（IO=1），退出循环，立即停止轴运动
        self.zmc.ZAux_Direct_Single_Cancel(axis)
        # 可选：发送急停/减速停止，Cancel是立即停止，也可用Stop做减速停止
        # self.zmc.ZAux_Direct_Single_Stop(axis)
        print(f"轴{axis}到达光电开关IO{io}，已停止运动")

    # ===== IO operations =====
    """读取单个输入 IO"""
    def get_input(self, io: int) -> int:
        self._require_connected()
        ret, val = self.zmc.ZAux_Direct_GetIn(io)
        if ret != 0:
            raise MotionError(f"GetIn failed, io={io}, ret={ret}")
        return val
