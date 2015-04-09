from Tkinter import *
import sys
import serial

################################
#main window widges
################################
class MainWindow(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.grid()
        self.ser = serial.Serial('com7', 9600)

        ###############################
        #widgets
        ###############################
        self.buttonConnect = Button(self,text="Unconected", command=self.buttonConnect_pressed)
        
        self.scaleRightlength=400
        self.scaleRightHip = Scale(self, label='Right Hip',length=self.scaleRightlength,sliderlength=10, command=self.onMove, from_=-60, to=60, resolution=0.1, orient='horizontal')
        self.scaleRightUpperLeg = Scale(self, label='Right Upper Leg',length=self.scaleRightlength,sliderlength=10, command=self.onMove, from_=-60, to=60, resolution=0.1, orient='horizontal')
        self.scaleRightMiddleLeg = Scale(self, label='Right Middle Leg',length=self.scaleRightlength,sliderlength=10, command=self.onMove, from_=-60, to=60, resolution=0.1, orient='horizontal')
        self.scaleRightKnee = Scale(self, label='Right Knee',length=self.scaleRightlength,sliderlength=10, command=self.onMove, from_=-60, to=60, resolution=0.1, orient='horizontal')
        self.scaleRightLowerLeg = Scale(self, label='Right Lower Leg',length=self.scaleRightlength,sliderlength=10, command=self.onMove, from_=-60, to=60, resolution=0.1, orient='horizontal')
        self.scaleRightAnkle= Scale(self, label='Right Ankle',length=self.scaleRightlength,sliderlength=10, command=self.onMove, from_=-60, to=60, resolution=0.1, orient='horizontal')

        self.scaleLeftlength=400
        self.scaleLeftHip = Scale(self, label='Left Hip',length=self.scaleLeftlength,sliderlength=10, command=self.onMove, from_=-60, to=60, resolution=0.1, orient='horizontal')
        self.scaleLeftUpperLeg = Scale(self, label='Left Upper Leg',length=self.scaleLeftlength,sliderlength=10, command=self.onMove, from_=-60, to=60, resolution=0.1, orient='horizontal')
        self.scaleLeftMiddleLeg = Scale(self, label='Left Middle Leg',length=self.scaleLeftlength,sliderlength=10, command=self.onMove, from_=-60, to=60, resolution=0.1, orient='horizontal')
        self.scaleLeftKnee = Scale(self, label='Left Knee',length=self.scaleLeftlength,sliderlength=10, command=self.onMove, from_=-60, to=60, resolution=0.1, orient='horizontal')
        self.scaleLeftLowerLeg = Scale(self, label='Left Lower Leg',length=self.scaleLeftlength,sliderlength=10, command=self.onMove, from_=-60, to=60, resolution=0.1, orient='horizontal')
        self.scaleLeftAnkle= Scale(self, label='Left Ankle',length=self.scaleLeftlength,sliderlength=10, command=self.onMove, from_=-60, to=60, resolution=0.1, orient='horizontal')


        ################################
        #positions on grid
        ################################
        self.scaleRightHip.grid(row=5,column=1)
        self.scaleRightUpperLeg.grid(row=6,column=1)
        self.scaleRightMiddleLeg.grid(row=7,column=1)
        self.scaleRightKnee.grid(row=8,column=1)
        self.scaleRightLowerLeg.grid(row=9,column=1)
        self.scaleRightAnkle.grid(row=10,column=1)

        self.scaleLeftHip.grid(row=5,column=2)
        self.scaleLeftUpperLeg.grid(row=6,column=2)
        self.scaleLeftMiddleLeg.grid(row=7,column=2)
        self.scaleLeftKnee.grid(row=8,column=2)
        self.scaleLeftLowerLeg.grid(row=9,column=2)
        self.scaleLeftAnkle.grid(row=10,column=2)

        self.buttonConnect.grid(row=1,column=1)

        
    def onMove(self, value):
        rh6='00'
        #rh6=chr(self.scaleRightHip.get())+chr(self.scaleRightHip.get())
        rul5='00'
        rml4='00'
        rk3='00'
        rll2='00'
        ra1='bb'

        lh6='00'
        lul5='00'
        lml4='00'
        lk3='00'
        lll2='00'
        la1='nt'
    
        mens='cmd'+rh6+rul5+rml4+rk3+rll2+ra1+lh6+lul5+lml4+lk3+lll2+la1
    
        ser.write('cmd')
        #print 'in onMove'

    def buttonConnect_pressed(self):
        self.ser = serial.Serial('COM7',9600)

            
        


if __name__ == '__main__':
    root=Tk()
    root.title("Robot Poser V1")
    root.geometry("800x600")
    MainWindow(root)
    root.mainloop() #root=Tkinter import *; root.mainloop()
