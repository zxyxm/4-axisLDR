import platform
import ctypes

# =========================================================
# DLL LOAD
# =========================================================
_systype = platform.system()
if _systype == "Windows":
    zauxdll = ctypes.WinDLL("./zauxdll.dll")
elif _systype == "Darwin":
    zauxdll = ctypes.CDLL("./zmotion.dylib")
elif _systype == "Linux":
    zauxdll = ctypes.CDLL("./libbzmotion.so")
else:
    raise RuntimeError("Unsupported OS")


# =========================================================
# ZMC NATIVE WRAPPER (1:1 API)
# =========================================================
class ZMCWrapper:
    def __init__(self):
        self.handle = ctypes.c_void_p()

    # ================= CONNECTION =================
    def ZAux_OpenEth(self, ip: str):
        ip_c = ctypes.c_char_p(ip.encode("utf-8"))
        return zauxdll.ZAux_OpenEth(ip_c, ctypes.byref(self.handle))

    def ZAux_Close(self):
        return zauxdll.ZAux_Close(self.handle)

    # ================= IO =================
    def ZAux_Direct_GetIn(self, ionum: int):
        val = ctypes.c_int()
        ret = zauxdll.ZAux_Direct_GetIn(self.handle, ionum, ctypes.byref(val))
        return ret, val.value

    def ZAux_Direct_SetOp(self, ionum: int, value: int):
        return zauxdll.ZAux_Direct_SetOp(self.handle, ionum, value)

    def ZAux_Direct_GetOp(self, ionum: int):
        val = ctypes.c_int()
        ret = zauxdll.ZAux_Direct_GetOp(self.handle, ionum, ctypes.byref(val))
        return ret, val.value

    def ZAux_Direct_MoveOp(self, ionum: int, value: int):
        return zauxdll.ZAux_Direct_MoveOp(self.handle, ionum, value)

    def ZAux_Direct_MoveOpMulti(self, ionum: int, mask: int, value: int):
        return zauxdll.ZAux_Direct_MoveOpMulti(
            self.handle, ionum, mask, value
        )

    def ZAux_Direct_MoveOp2(self, ionum: int, value: int, delay_ms: int):
        return zauxdll.ZAux_Direct_MoveOp2(
            self.handle, ionum, value, delay_ms
        )

    def ZAux_GetModbusIn(self, start: int, num: int):
        buf = (ctypes.c_int * num)()
        ret = zauxdll.ZAux_GetModbusIn(self.handle, start, num, buf)
        return ret, list(buf)

    def ZAux_GetInMulti(self, start: int, num: int):
        buf = (ctypes.c_int * num)()
        ret = zauxdll.ZAux_GetInMulti(self.handle, start, num, buf)
        return ret, list(buf)

    def ZAux_GetModbusOut(self, start: int, num: int):
        buf = (ctypes.c_int * num)()
        ret = zauxdll.ZAux_GetModbusOut(self.handle, start, num, buf)
        return ret, list(buf)

    # ================= AXIS PARAM =================

    def ZAux_Direct_SetAtype(self, axis: int, value: int):
        return zauxdll.ZAux_Direct_SetAtype(self.handle, axis, value)

    def ZAux_Direct_GetAtype(self, axis: int):
        val = ctypes.c_int()
        ret = zauxdll.ZAux_Direct_GetAtype(self.handle, axis, ctypes.byref(val))
        return ret, val.value

    def ZAux_Direct_SetUnits(self, axis: int, value: float):
        return zauxdll.ZAux_Direct_SetUnits(
            self.handle, axis, ctypes.c_float(value)
        )

    def ZAux_Direct_GetUnits(self, axis: int):
        val = ctypes.c_float()
        ret = zauxdll.ZAux_Direct_GetUnits(
            self.handle, axis, ctypes.byref(val)
        )
        return ret, val.value

    def ZAux_Direct_SetSpeed(self, axis: int, value: float):
        return zauxdll.ZAux_Direct_SetSpeed(
            self.handle, axis, ctypes.c_float(value)
        )

    def ZAux_Direct_GetSpeed(self, axis: int):
        val = ctypes.c_float()
        ret = zauxdll.ZAux_Direct_GetSpeed(
            self.handle, axis, ctypes.byref(val)
        )
        return ret, val.value

    def ZAux_Direct_SetAccel(self, axis: int, value: float):
        return zauxdll.ZAux_Direct_SetAccel(
            self.handle, axis, ctypes.c_float(value)
        )
    
    def ZAux_Direct_GetAccel(self, axis: int):
        val = ctypes.c_float()
        ret = zauxdll.ZAux_Direct_GetAccel(
            self.handle, axis, ctypes.byref(val)
        )
        return ret, val.value

    def ZAux_Direct_SetDecel(self, axis: int, value: float):
        return zauxdll.ZAux_Direct_SetDecel(
            self.handle, axis, ctypes.c_float(value)
        )
    
    def ZAux_Direct_GetDecel(self, axis: int):
        val = ctypes.c_float()
        ret = zauxdll.ZAux_Direct_GetDecel(
            self.handle, axis, ctypes.byref(val)
        )
        return ret, val.value

    def ZAux_Direct_SetSramp(self, axis: int, value: float):
        return zauxdll.ZAux_Direct_SetSramp(
            self.handle, axis, ctypes.c_float(value)
        )

    def ZAux_Direct_GetSramp(self, axis: int):
        val = ctypes.c_float()
        ret = zauxdll.ZAux_Direct_GetSramp(
            self.handle, axis, ctypes.byref(val)
        )
        return ret, val.value


    # ================= STATUS =================

    def ZAux_Direct_GetIfIdle(self, axis: int):
        val = ctypes.c_int()
        ret = zauxdll.ZAux_Direct_GetIfIdle(
            self.handle, axis, ctypes.byref(val)
        )
        return ret, val.value

    def ZAux_Direct_GetAxisStatus(self, axis: int):
        val = ctypes.c_int()
        ret = zauxdll.ZAux_Direct_GetAxisStatus(
            self.handle, axis, ctypes.byref(val)
        )
        return ret, val.value

    def ZAux_Direct_SetDpos(self, axis: int, value: float):
        return zauxdll.ZAux_Direct_SetDpos(
            self.handle, axis, ctypes.c_float(value)
        )

    def ZAux_Direct_GetDpos(self, axis: int):
        val = ctypes.c_float()
        ret = zauxdll.ZAux_Direct_GetDpos(
            self.handle, axis, ctypes.byref(val)
        )
        return ret, val.value
    
    def ZAux_Direct_SetMpos(self, axis: int, value: float):
        return zauxdll.ZAux_Direct_SetMpos(
            self.handle, axis, ctypes.c_float(value)
        )
    
    def ZAux_Direct_GetMpos(self, axis: int):
        val = ctypes.c_float()
        ret = zauxdll.ZAux_Direct_GetMpos(
            self.handle, axis, ctypes.byref(val)
        )
        return ret, val.value
    # ================= SINGLE AXIS MOTION =================

    def ZAux_Direct_Single_Vmove(self, axis: int, direction: int):
        return zauxdll.ZAux_Direct_Single_Vmove(self.handle, axis, direction)

    def ZAux_Direct_Single_Move(self, axis: int, distance: float):
        return zauxdll.ZAux_Direct_Single_Move(
            self.handle, axis, ctypes.c_float(distance)
        )

    def ZAux_Direct_Single_MoveAbs(self, axis: int, pos: float):
        return zauxdll.ZAux_Direct_Single_MoveAbs(
            self.handle, axis, ctypes.c_float(pos)
        )

    def ZAux_Direct_Single_Cancel(self, axis: int, mode: int = 0):
        return zauxdll.ZAux_Direct_Single_Cancel(self.handle, axis, mode)
    
    # ================= HOME / DATUM =================
    def ZAux_Direct_Single_Datum(self, axis: int, mode: int):
        return zauxdll.ZAux_Direct_Single_Datum(
            self.handle, axis, mode
        )

    def ZAux_Direct_SetCreep(self, axis: int, value: float):
        return zauxdll.ZAux_Direct_SetCreep(
            self.handle, axis, ctypes.c_float(value)
        )

    def ZAux_Direct_GetCreep(self, axis: int):
        val = ctypes.c_float()
        ret = zauxdll.ZAux_Direct_GetCreep(
            self.handle, axis, ctypes.byref(val)
        )
        return ret, val.value

    def ZAux_Direct_SetDatumIn(self, axis: int, ionum: int):
        return zauxdll.ZAux_Direct_SetDatumIn(
            self.handle, axis, ionum
        )

    def ZAux_Direct_GetDatumIn(self, axis: int):
        val = ctypes.c_int()
        ret = zauxdll.ZAux_Direct_GetDatumIn(
            self.handle, axis, ctypes.byref(val)
        )
        return ret, val.value

    def ZAux_Direct_SetHomeWait(self, axis: int, value: int):
        return zauxdll.ZAux_Direct_SetHomeWait(
            self.handle, axis, value
        )

    def ZAux_Direct_GetHomeWait(self, axis: int):
        val = ctypes.c_int()
        ret = zauxdll.ZAux_Direct_GetHomeWait(
            self.handle, axis, ctypes.byref(val)
        )
        return ret, val.value
    
    def ZAux_Direct_SetFwdIn(self, axis: int, io: int) -> int:
        return zauxdll.ZAux_Direct_SetFwdIn(
            self.handle, axis, ctypes.c_int(io)
        )

    def ZAux_Direct_GetFwdIn(self, axis: int):
        val = ctypes.c_int()
        ret = zauxdll.ZAux_Direct_GetFwdIn(
            self.handle, axis, ctypes.byref(val)
        )
        return ret, val.value

    def ZAux_Direct_SetRevIn(self, axis: int, io: int) -> int:
        return zauxdll.ZAux_Direct_SetRevIn(
            self.handle, axis, ctypes.c_int(io)
        )

    def ZAux_Direct_GetRevIn(self, axis: int):
        val = ctypes.c_int()
        ret = zauxdll.ZAux_Direct_GetRevIn(
            self.handle, axis, ctypes.byref(val)
        )
        return ret, val.value

    def ZAux_Direct_SetInvertIn(self, ionum: int, invert: int):
        return zauxdll.ZAux_Direct_SetInvertIn(
            self.handle, ionum, invert
        )

    def ZAux_Direct_GetInvertIn(self, ionum: int):
        val = ctypes.c_int()
        ret = zauxdll.ZAux_Direct_GetInvertIn(
            self.handle, ionum, ctypes.byref(val)
        )
        return ret, val.value

    # ================= MULTI AXIS INTERPOLATION =================
    def ZAux_Direct_Move(self, n ,axislist, dislist):
        alist = (ctypes.c_int * n)(*axislist)
        dlist = (ctypes.c_float * n)(*dislist)
        return zauxdll.ZAux_Direct_Move(self.handle, n, alist, dlist)

    def ZAux_Direct_MoveSp(self, n, axislist, dislist):
        alist = (ctypes.c_int * n)(*axislist)
        dlist = (ctypes.c_float * n)(*dislist)
        return zauxdll.ZAux_Direct_MoveSp(self.handle, n, alist, dlist)

    def ZAux_Direct_MoveAbs(self, n, axislist, dislist):
        alist = (ctypes.c_int * n)(*axislist)
        dlist = (ctypes.c_float * n)(*dislist)
        return zauxdll.ZAux_Direct_MoveAbs(self.handle, n, alist, dlist)
    
    def ZAux_Direct_MoveCirc2(self, n, axislist, fmid1, fmid2, fend1, fend2):
        alist = (ctypes.c_int * n)(*axislist)
        return zauxdll.ZAux_Direct_MoveCirc2(
            self.handle, n, alist,
            ctypes.c_float(fmid1), ctypes.c_float(fmid2),
            ctypes.c_float(fend1), ctypes.c_float(fend2)
        )

    def ZAux_Direct_MoveCirc2Sp(self, n, axislist, fmid1, fmid2, fend1, fend2):
        alist = (ctypes.c_int * n)(*axislist)
        alist = (ctypes.c_int * n)(*axislist)
        return zauxdll.ZAux_Direct_MoveCirc2Sp(
            self.handle, n, alist,
            ctypes.c_float(fmid1), ctypes.c_float(fmid2),
            ctypes.c_float(fend1), ctypes.c_float(fend2)
        )

    def ZAux_Direct_MoveCirc2Abs(self, n, axislist, fmid1, fmid2, fend1, fend2):
        alist = (ctypes.c_int * n)(*axislist)
        return zauxdll.ZAux_Direct_MoveCirc2Abs(
            self.handle, n, alist,
            ctypes.c_float(fmid1), ctypes.c_float(fmid2),
            ctypes.c_float(fend1), ctypes.c_float(fend2)
        )

    def ZAux_Direct_MoveCirc2AbSp(self, n, axislist, fmid1, fmid2, fend1, fend2):
        alist = (ctypes.c_int * n)(*axislist)
        return zauxdll.ZAux_Direct_MoveCirc2AbSp(
            self.handle, n, alist,
            ctypes.c_float(fmid1), ctypes.c_float(fmid2),
            ctypes.c_float(fend1), ctypes.c_float(fend2)
        )

    def ZAux_Direct_MoveCircAbs(self, n, axislist, fmid1, fmid2, fend1, fend2, direction):
        alist = (ctypes.c_int * n)(*axislist)
        return zauxdll.ZAux_Direct_MoveCircAbs(
            self.handle, n, alist,
            ctypes.c_float(fmid1), ctypes.c_float(fmid2),
            ctypes.c_float(fend1), ctypes.c_float(fend2),
            ctypes.c_int(direction)
        )

    def ZAux_Direct_MSpherical(self, n, axislist, cx, cy, cz, ex, ey, ez, mode):
        alist = (ctypes.c_int * n)(*axislist)
        return zauxdll.ZAux_Direct_MSpherical(
            self.handle, n, alist,
            ctypes.c_float(cx), ctypes.c_float(cy), ctypes.c_float(cz),
            ctypes.c_float(ex), ctypes.c_float(ey), ctypes.c_float(ez),
            ctypes.c_int(mode)
        )


    def ZAux_Direct_MSphericalSp(self, n, axislist, c1, c2, c3, e1, e2, e3, mode, extra1, extra2):
        alist = (ctypes.c_int * n)(*axislist)
        return zauxdll.ZAux_Direct_MSphericalSp(
            self.handle, n, alist,
            ctypes.c_float(c1), ctypes.c_float(c2), ctypes.c_float(c3),
            ctypes.c_float(e1), ctypes.c_float(e2), ctypes.c_float(e3),
            ctypes.c_int(mode),
            ctypes.c_float(extra1), ctypes.c_float(extra2)
        )


    def ZAux_Direct_MHelical(self, n, axislist, start1, start2, center1, center2, distance3, direction, mode):
        alist = (ctypes.c_int * n)(*axislist)
        return zauxdll.ZAux_Direct_MHelical(
            self.handle, n, alist,
            ctypes.c_float(start1), ctypes.c_float(start2),
            ctypes.c_float(center1), ctypes.c_float(center2),
            ctypes.c_float(distance3),
            ctypes.c_int(direction),
            ctypes.c_int(mode)
        )

    def ZAux_Direct_MHelicalSp(self, n, axislist, end1, end2, center1, center2, direction, distance3, mode):
        alist = (ctypes.c_int * n)(*axislist)
        return zauxdll.ZAux_Direct_MHelicalSp(
            self.handle, n, alist,
            ctypes.c_float(end1), ctypes.c_float(end2),
            ctypes.c_float(center1), ctypes.c_float(center2),
            ctypes.c_int(direction),
            ctypes.c_float(distance3),
            ctypes.c_int(mode)
        )

    def ZAux_Direct_MHelicalSp(self, n, axislist, end1, end2, center1, center2, direction, distance3, mode):
        alist = (ctypes.c_int * n)(*axislist)
        return zauxdll.ZAux_Direct_MHelicalSp(
            self.handle, n, alist,
            ctypes.c_float(end1), ctypes.c_float(end2),
            ctypes.c_float(center1), ctypes.c_float(center2),
            ctypes.c_int(direction),
            ctypes.c_float(distance3),
            ctypes.c_int(mode)
        )

    def ZAux_Direct_MHelicalAbsSp(self, n, axislist, end1, end2, center1, center2, direction, distance3, mode):
        alist = (ctypes.c_int * n)(*axislist)
        return zauxdll.ZAux_Direct_MHelicalAbsSp(
            self.handle, n, alist,
            ctypes.c_float(end1), ctypes.c_float(end2),
            ctypes.c_float(center1), ctypes.c_float(center2),
            ctypes.c_int(direction),
            ctypes.c_float(distance3),
            ctypes.c_int(mode)
        )

    def ZAux_Direct_MHelical2(self, n, axislist, end1, end2, end3, end4, distance5, mode):
        alist = (ctypes.c_int * n)(*axislist)
        return zauxdll.ZAux_Direct_MHelical2(
            self.handle, n, alist,
            ctypes.c_float(end1), ctypes.c_float(end2),
            ctypes.c_float(end3), ctypes.c_float(end4),
            ctypes.c_float(distance5),
            ctypes.c_int(mode)
        )
    
    def ZAux_Direct_MHelical2Sp(self, n, axislist, end1, end2, end3, end4, distance5, mode):
        alist = (ctypes.c_int * n)(*axislist)
        return zauxdll.ZAux_Direct_MHelical2Sp(
            self.handle, n, alist,
            ctypes.c_float(end1), ctypes.c_float(end2),
            ctypes.c_float(end3), ctypes.c_float(end4),
            ctypes.c_float(distance5),
            ctypes.c_int(mode)
        )

    def ZAux_Direct_MHelical2Abs(self, n, axislist, end1, end2, end3, end4, distance5, mode):
        alist = (ctypes.c_int * n)(*axislist)
        return zauxdll.ZAux_Direct_MHelical2Abs(
            self.handle, n, alist,
            ctypes.c_float(end1), ctypes.c_float(end2),
            ctypes.c_float(end3), ctypes.c_float(end4),
            ctypes.c_float(distance5),
            ctypes.c_int(mode)
        )

    def ZAux_Direct_MHelical2AbsSp(self, n, axislist, end1, end2, end3, end4, distance5, mode):
        alist = (ctypes.c_int * n)(*axislist)
        return zauxdll.ZAux_Direct_MHelical2AbsSp(
            self.handle, n, alist,
            ctypes.c_float(end1), ctypes.c_float(end2),
            ctypes.c_float(end3), ctypes.c_float(end4),
            ctypes.c_float(distance5),
            ctypes.c_int(mode)
        )

    def ZAux_Direct_MEclipse(self, *args):
        return zauxdll.ZAux_Direct_MEclipse(self.handle, *args)

    def ZAux_Direct_MEclipseSp(self, *args):
        return zauxdll.ZAux_Direct_MEclipseSp(self.handle, *args)

    def ZAux_Direct_MEclipseAbs(self, *args):
        return zauxdll.ZAux_Direct_MEclipseAbs(self.handle, *args)

    def ZAux_Direct_MEclipseAbsSp(self, *args):
        return zauxdll.ZAux_Direct_MEclipseAbsSp(self.handle, *args)

    def ZAux_Direct_MEclipseHelical(self, *args):
        return zauxdll.ZAux_Direct_MEclipseHelical(self.handle, *args)

    def ZAux_Direct_MEclipseHelicalSp(self, *args):
        return zauxdll.ZAux_Direct_MEclipseHelicalSp(self.handle, *args)

    def ZAux_Direct_MEclipseHelicalAbs(self, *args):
        return zauxdll.ZAux_Direct_MEclipseHelicalAbs(self.handle, *args)

    def ZAux_Direct_MEclipseHelicalAbsSp(self, *args):
        return zauxdll.ZAux_Direct_MEclipseHelicalAbsSp(self.handle, *args)

    def ZAux_Direct_MoveSpiral(self, *args):
        return zauxdll.ZAux_Direct_MoveSpiral(self.handle, *args)

    def ZAux_Direct_MoveSpiralSp(self, *args):
        return zauxdll.ZAux_Direct_MoveSpiralSp(self.handle, *args)

    def ZAux_Direct_MoveTurnabs(self, *args):
        return zauxdll.ZAux_Direct_MoveTurnabs(self.handle, *args)

    def ZAux_Direct_McircTurnabs(self, *args):
        return zauxdll.ZAux_Direct_McircTurnabs(self.handle, *args)

    def ZAux_Direct_MoveASynmove(self, *args):
        return zauxdll.ZAux_Direct_MoveASynmove(self.handle, *args)

    def ZAux_Direct_MoveSynmove(self, *args):
        return zauxdll.ZAux_Direct_MoveSynmove(self.handle, *args)

    def ZAux_Direct_Rapidstop(self):
        return zauxdll.ZAux_Direct_Rapidstop(self.handle)

    def ZAux_Direct_CancelAxisList(self, axislist):
        n = len(axislist)
        a = (ctypes.c_int * n)(*axislist)
        return zauxdll.ZAux_Direct_CancelAxisList(self.handle, n, a)

    def ZAux_Trigger(self):
        return zauxdll.ZAux_Trigger(self.handle)
