#Initial-T 2019.6
import serial
import time
  
ACCData=[0.0]*8
GYROData=[0.0]*8
AngleData=[0.0]*8         
  
FrameState = 0            
Bytenum = 0               
CheckSum = 0                     

def DueData(inputdata):   
    global  FrameState    
    global  Bytenum
    global  CheckSum
    for data in inputdata:  
        if FrameState==0:   
            if data==0x55 and Bytenum==0: 
                CheckSum=data
                Bytenum=1
                continue
            elif data==0x51 and Bytenum==1:
                CheckSum+=data
                FrameState=1
                Bytenum=2
            elif data==0x52 and Bytenum==1: 
                CheckSum+=data
                FrameState=2
                Bytenum=2
            elif data==0x53 and Bytenum==1:
                CheckSum+=data
                FrameState=3
                Bytenum=2
        elif FrameState==1: 
            if Bytenum<10:          
                ACCData[Bytenum-2]=data 
                CheckSum+=data
                Bytenum+=1
            else:
                CheckSum=0                 
                Bytenum=0
                FrameState=0
        elif FrameState==2: 
            if Bytenum<10:
                GYROData[Bytenum-2]=data
                CheckSum+=data
                Bytenum+=1
            else:
                CheckSum=0
                Bytenum=0
                FrameState=0
        elif FrameState==3: # angle
            if Bytenum<10:
                AngleData[Bytenum-2]=data
                CheckSum+=data
                Bytenum+=1
            else:
                if data == (CheckSum&0xff):
                    roll,pitch,yaw = get_angle(AngleData)
                CheckSum=0
                Bytenum=0
                FrameState=0
                if get_angle(AngleData) is not None:
                    return roll,pitch,yaw
def get_angle(datahex):                          
    rxl = datahex[0]                                       
    rxh = datahex[1]
    ryl = datahex[2]                                       
    ryh = datahex[3]
    rzl = datahex[4]                                       
    rzh = datahex[5]
    k_angle = 180
  
    angle_x = (rxh << 8 | rxl) / 32768 * k_angle
    angle_y = (ryh << 8 | ryl) / 32768 * k_angle
    angle_z = (rzh << 8 | rzl) / 32768 * k_angle
    if angle_x >= k_angle:
        angle_x -= 2 * k_angle
    if angle_y >= k_angle:
        angle_y -= 2 * k_angle
    if angle_z >=k_angle:
        angle_z-= 2 * k_angle
  
    return angle_x,angle_y,angle_z
  



if __name__ == 'main':
    DueData()