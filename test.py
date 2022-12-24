import serial
import numpy as np 
import pandas as pd
import time 
from dynamixel_sdk import *
from tkinter import *
import Denem2 


present3= [525, 490, 500 ,490, 530, 505, 500, 490, 540, 495, 530, 520] # En güncel hali Dik Duruş
present4 = [525, 490, (500-101), (490-10), (535-139), (505-112), (460-38), (450-102), 530, 495, 525, 520] # Yürümeye başlangıç pozisyonu 


df = pd.read_excel('/home/berkay/Desktop/Ruby-Main-Code/minisarkac.xls')

dfm = (np.array(df)/0.293)

ser = serial.Serial('/dev/rfcomm0',115200,timeout=0.5)
portHandler = PortHandler('/dev/ttyUSB0')
packetHandler = PacketHandler(1)
portHandler.openPort()
portHandler.setBaudRate(1000000)

if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")

if portHandler.setBaudRate(1000000):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")

def Euler():
    while(1):
        datahex = ser.read(33)
        roll , pitch , yaw = Denem2.DueData(datahex)
        return round(roll)
        #print(f'roll : {round(roll) :<30} pitch : {round(pitch) :<30} yaw : {round(yaw) :<30}')

def TorqueEnable():
    for j in range(1,13):
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, j, 24, 1)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel has been successfully connected")
     

def ToqueDisable():
    for i in range(1,13):
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler,i, 24, 0)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))


def prepareToWalk():
    for i in range(1,13):
        packetHandler.write2ByteTxRx(portHandler, i, 32, 0)
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, i, 30, present4[i-1])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))


def walking():
    for i in range(0,51,3):
        for j in range(0,12):
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,j+1,30,present4[j] + round(dfm[i][j]))
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))
            
def standUpright():
    for i in range(1,13):
        packetHandler.write2ByteTxRx(portHandler, i, 32, 100)
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, i, 30, present3[i-1])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

def breakKnee():
    bk =  [525,490,440,430,403,385,400,390,540,495,503,520]
    for i in range(1,13):
        packetHandler.write2ByteTxRx(portHandler, i, 32, 100)
        packetHandler.write2ByteTxRx(portHandler, i, 30, bk[i-1])

def start_Balance():
    while (1): 
        preposition_ID3 = packetHandler.read2ByteTxRx(portHandler,3,36)
        preposition_ID4 = packetHandler.read2ByteTxRx(portHandler,4,36)
        preposition_ID7 = packetHandler.read2ByteTxRx(portHandler,7,36)
        preposition_ID8 = packetHandler.read2ByteTxRx(portHandler,8,36)
        if Euler() > 25 or Euler() < -25:
            if packetHandler.read1ByteTxRx(portHandler,3,46) == 0:                              # Moving Status 
                packetHandler.write2ByteTxRx(portHandler,3,(preposition_ID3+(Euler()/0.293)))
            if packetHandler.read1ByteTxRx(portHandler,4,46) == 0:                              # Moving Status
                packetHandler.write2ByteTxRx(portHandler,4,(preposition_ID4+(Euler()/0.293)))
            if packetHandler.read1ByteTxRx(portHandler,7,46) == 0:
                packetHandler.write2ByteTxRx(portHandler,7,(preposition_ID7+(Euler()/0.293)))
            if packetHandler.read1ByteTxRx(portHandler,8,46) == 0:
                packetHandler.write2ByteTxRx(portHandler,8,(preposition_ID8+(Euler()/0.293)))
        else :
            if packetHandler.read1ByteTxRx(portHandler,3,46) == 0:
                packetHandler.write2ByteTxRx(portHandler,3,(preposition_ID3+(Euler()/0.293)))
            if packetHandler.read1ByteTxRx(portHandler,4,46) == 0:
                packetHandler.write2ByteTxRx(portHandler,4,(preposition_ID4+(Euler()/0.293)))


    #while(1):
    #    counter = 1
    #    data = list()
    #    data[counter], dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(
    #        portHandler, counter, 36)
    #    if counter == 12:
    #        counter = 0
    #    if dxl_comm_result != COMM_SUCCESS:
    #        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    #    elif dxl_error != 0:
    #        print("%s" % packetHandler.getRxPacketError(dxl_error))
    #    counter = counter + 1
    #    
    #    List.insert(data[0])
    #    List1.insert(data[1])
    #    List2.insert(data[2])
    #    List3.insert(data[3])
    #    List4.insert(data[4])
    #    List5.insert(data[5])
    #    List6.insert(data[6])
    #    List7.insert(data[7])
    #    List8.insert(data[8])
    #    List9.insert(data[9])
    #    List10.insert(data[10])
    #    List11.insert(data[11])
    #    
    #   
    #time.sleep(0.8)
        
        

#---------------------------------------------------------------------------------Grafic Unit Interface----------------------------------------------------------------------------------------------------
master = Tk()
master.title('RUBY Graphic Unit Interface')

master.geometry('640x480')

bg = PhotoImage(file='/home/berkay/Desktop/Ruby-Main-Code/deulogo.png')
label1 = Label( master, image = bg)
label1.place(relx=0.3,rely=0.25)

walk_Button = Button(master,  text='Walking' , command= walking,fg='white',bg='black')
walk_Button.place(x=10,y=10)

standUpright_button = Button(master,text='Stand UpRight',command=standUpright,fg='white',bg='black')
standUpright_button.place(x=80,y=10)

prepareToWalk_button = Button(master,text='Prepare To Walk',command=prepareToWalk,fg='white',bg='black')
prepareToWalk_button.place(x=180,y=10)

TorqueEnable_button = Button(master,text='Torque Enable',command=TorqueEnable,fg='white',bg='black')
TorqueEnable_button.place(x=290,y=10)

TorqueDisable_button = Button(master,text='Torque Disable',command=ToqueDisable,fg='white',bg='black')
TorqueDisable_button.place(x=390,y=10)

breakKnee_button= Button(master,text='Break Knee',command=breakKnee,fg='white',bg='black')
breakKnee_button.place(x=500,y=10)

startBalanced_button= Button(master,text='Start Balanced',command=start_Balance,fg='white',bg='black')
startBalanced_button.place(x=500,y=100)

iD_1 = Label(master,text='ID 1 : ')
iD_1.place(x=10,y=90)
List = Listbox(master,width=8,height=1)
List.place(x=40,y=90)

iD_2 = Label(master,text='ID 2 : ')
iD_2.place(x=10,y=130)
List1 = Listbox(master,width=8,height=1)
List1.place(x=40,y=130)

iD_3 = Label(master,text='ID 3 : ')
iD_3.place(x=10,y=170)
List2 = Listbox(master,width=8,height=1)
List2.place(x=40,y=170)

iD_4 = Label(master,text='ID 4 : ')
iD_4.place(x=10,y=210)
List3 = Listbox(master,width=8,height=1)
List3.place(x=40,y=210)

iD_5 = Label(master,text='ID 5 : ')
iD_5.place(x=10,y=250)
List4 = Listbox(master,width=8,height=1)
List4.place(x=40,y=250)

iD_6 = Label(master,text='ID 6 : ')
iD_6.place(x=10,y=290)
List5 = Listbox(master,width=8,height=1)
List5.place(x=40,y=290)

iD_7 = Label(master,text='ID 7 : ')
iD_7.place(x=90,y=90)
List6 = Listbox(master,width=8,height=1)
List6.place(x=120,y=90)

iD_8 = Label(master,text='ID 8 : ')
iD_8.place(x=90,y=130)
List7 = Listbox(master,width=8,height=1)
List7.place(x=120,y=130)

iD_9 = Label(master,text='ID 9 : ')
iD_9.place(x=90,y=170)
List8 = Listbox(master,width=8,height=1)
List8.place(x=120,y=170)

iD_10 = Label(master,text='ID 10 : ')
iD_10.place(x=90,y=210)
List9 = Listbox(master,width=8,height=1)
List9.place(x=120,y=210)

iD_11 = Label(master,text='ID 11 : ')
iD_11.place(x=90,y=250)
List10 = Listbox(master,width=8,height=1)
List10.place(x=120,y=250)

iD_12 = Label(master,text='ID 12 : ')
iD_12.place(x=90,y=290)
List11 = Listbox(master,width=8,height=1)
List11.place(x=120,y=290)

master.mainloop()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





    

     