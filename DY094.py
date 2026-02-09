from pymodbus.client import ModbusSerialClient
# 核心修改：修正ModbusRtuFramer的导入路径
from pymodbus.framer.rtu_framer import ModbusRtuFramer  
from pymodbus.exceptions import ModbusException
import struct

class DY094Reader:
    def __init__(self, port, slave_id=1, baudrate=19200):
        """初始化DY094变送器客户端（适配新版pymodbus 3.x+）"""
        # 核心修改：移除method，新增framer=ModbusRtuFramer
        self.client = ModbusSerialClient(
            port=port,          # 串口地址（Windows：COM3/COM4；Linux：/dev/ttyUSB0）
            framer=ModbusRtuFramer,  # 替换原method='rtu'，指定RTU帧格式
            baudrate=baudrate,  # 默认19200（DY094手册默认波特率）
            parity='N',         # 无校验（8N1）
            stopbits=1,         # 1停止位
            bytesize=8,         # 8数据位
            timeout=1           # 超时时间（秒）
        )
        self.slave_id = slave_id  # 默认从站地址1

    def connect(self):
        """连接变送器"""
        if self.client.connect():
            print("✅ 变送器连接成功！")
            return True
        else:
            print("❌ 变送器连接失败，请检查：1.串口地址 2.接线 3.通信参数")
            return False

    def disconnect(self):
        """断开连接"""
        self.client.close()
        print("🔌 连接已断开")

    def _bytes_to_long(self, byte_data):
        """将4字节数据转换为Long型（手册要求高位在前）"""
        return struct.unpack('>i', byte_data)[0]

    def _bytes_to_float(self, byte_data):
        """将4字节数据转换为Float型（手册要求高位在前）"""
        return struct.unpack('>f', byte_data)[0]

    def read_single_channel(self, channel=1, data_type='long'):
        """
        读取单个通道测量值
        :param channel: 通道号（1-9）
        :param data_type: 数据类型（'long' 或 'float'）
        :return: 十进制测量值
        """
        if not (1 <= channel <= 9):
            print("❌ 通道号必须为1-9")
            return None

        # 手册参数表：测量值Long型地址=768+2*(channel-1)，Float型地址=256+2*(channel-1)
        if data_type == 'long':
            start_addr = 768 + 2 * (channel - 1)
        elif data_type == 'float':
            start_addr = 256 + 2 * (channel - 1)
        else:
            print("❌ 数据类型仅支持 'long' 或 'float'")
            return None

        try:
            # 读取2个寄存器（4字节，手册要求读取个数为2的倍数）
            response = self.client.read_holding_registers(
                address=start_addr,
                count=2,
                slave=self.slave_id
            )

            if response.isError():
                print(f"❌ 读取失败：{response}")
                return None

            # 提取寄存器数据并转换为字节流（高位在前）
            reg_data = response.registers
            byte_data = struct.pack('>HH', reg_data[0], reg_data[1])  # 2个16位寄存器→4字节

            # 按数据类型转换
            if data_type == 'long':
                value = self._bytes_to_long(byte_data)
            else:
                value = self._bytes_to_float(byte_data)

            print(f"📊 通道{channel}（{data_type}型）测量值：{value}")
            return value

        except ModbusException as e:
            print(f"❌ Modbus通信异常：{e}")
            return None
        except Exception as e:
            print(f"❌ 未知异常：{e}")
            return None

    def read_all_channels(self, data_type='long'):
        """
        读取所有9个通道测量值
        :param data_type: 数据类型（'long' 或 'float'）
        :return: 字典{通道号: 测量值}
        """
        print(f"\n📋 开始读取所有9通道（{data_type}型）...")
        results = {}

        # 手册参数表：9通道连续地址（Long型起始768，Float型起始256，共18个寄存器=9通道×2）
        if data_type == 'long':
            start_addr = 768
        elif data_type == 'float':
            start_addr = 256
        else:
            print("❌ 数据类型仅支持 'long' 或 'float'")
            return results

        try:
            # 读取18个寄存器（9通道×2个寄存器/通道）
            response = self.client.read_holding_registers(
                address=start_addr,
                count=18,
                slave=self.slave_id
            )

            if response.isError():
                print(f"❌ 批量读取失败：{response}")
                return results

            reg_data = response.registers
            # 每2个寄存器对应1个通道（4字节）
            for i in range(9):
                channel = i + 1
                # 提取当前通道的2个寄存器
                channel_regs = reg_data[i*2 : (i+1)*2]
                byte_data = struct.pack('>HH', channel_regs[0], channel_regs[1])
                
                if data_type == 'long':
                    value = self._bytes_to_long(byte_data)
                else:
                    value = self._bytes_to_float(byte_data)
                
                results[channel] = value
                print(f"通道{channel}：{value}")

            return results

        except ModbusException as e:
            print(f"❌ Modbus通信异常：{e}")
            return results
        except Exception as e:
            print(f"❌ 未知异常：{e}")
            return results
def main():
    reader = DY094Reader(port='COM4')  # Windows示例，确认你的485模块对应COM口

    if reader.connect():
        # 1. 读取单通道（通道1，Long型）
        reader.read_single_channel(channel=1, data_type='long')
        
        # 2. 读取单通道（通道1，Float型）
        reader.read_single_channel(channel=1, data_type='float')
        
        # 3. 读取所有9通道（Long型）
        reader.read_all_channels(data_type='long')
        
        # 4. 读取所有9通道（Float型）
        reader.read_all_channels(data_type='float')

        # 断开连接
        reader.disconnect()

# --------------------------
# 测试代码（Windows系统适配）
# --------------------------
if __name__ == "__main__":
    # 初始化客户端（根据实际串口地址修改port参数，如COM3/COM4）
    main()