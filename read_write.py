import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

def SDK(motor_ID,goal,portHandler,packetHandler):
    
    ADDR_MX_TORQUE_ENABLE = 24
    ADDR_MX_GOAL_POSITION = 30
    ADDR_MX_PRESENT_POSITION = 36

    # Default setting
    DXL_ID = motor_ID                      
    TORQUE_ENABLE = 1                
    dxl_goal_position =  goal      


    # Enable Dynamixel Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        
        # Write goal position
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(
        portHandler, DXL_ID, ADDR_MX_GOAL_POSITION, dxl_goal_position)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        
   # # Read present positio
   # dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(
   #     portHandler, DXL_ID, ADDR_MX_PRESENT_POSITION)
   # if dxl_comm_result != COMM_SUCCESS:
   #     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
   # elif dxl_error != 0:
   #     print("%s" % packetHandler.getRxPacketError(dxl_error))
   # print("[ID:%03d] GoalPos:%03d  PresPos:%03d" %
   #     (DXL_ID, dxl_goal_position, dxl_present_position))


if __name__ == '__main__':
    SDK()
