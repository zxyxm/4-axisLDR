# main.py
import time
from motion import Motion, MotionError, MotionTimeout

def main():
    ip = "192.168.0.11"
    axes = [0, 1, 2]  # 三轴一次性归零

    motion = Motion(ip)

    try:
        # ===== connect =====
        motion.connect()

        # ===== axis basic setup =====
        for ax in axes:
            motion.set_axis(
                axis=ax,
                atype=1,     # 脉冲轴
                speed=100,   # 速度
                units=100,   # 脉冲当量
                accel=200,   # 加速度
                decel=200,   # 减速度
                sramp=1000,
                dpos=0       # 初始 DPOS
            )

        # ===== home configuration =====
        home_inputs = [18, 22, 24]    
        home_modes = [3, 3, 4]        

        for ax, hi in zip(axes, home_inputs):
            motion.set_home(
                axis=ax,
                home_input=hi,
                home_wait=100,
                invert_level=0,
                creep_speed=10,
                fwd_limit_in=6,
                rev_limit_in=6
            )

        # ===== homing =====
        for ax, mode in zip(axes, home_modes):
            motion.home(
                axis=ax,
                mode=mode,
                timeout=20.0
            )

        # ===== read position after homing =====
        for ax in axes:
            dpos, mpos = motion.get_pos(ax)
            print(f"Axis {ax} homed. DPOS={dpos}, MPOS={mpos}")

    except MotionTimeout as e:
        print(f"[TIMEOUT] {e}")
    except MotionError as e:
        print(f"[MOTION ERROR] {e}")
    finally:
        motion.close()


if __name__ == "__main__":
    main()
