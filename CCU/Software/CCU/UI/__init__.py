
import sys, random

import serial, time

from PySide import QtGui, QtCore

class Base(QtGui.QWidget):
    
    def __init__(self):
        super(Base, self).__init__()
        
        self.initUI()
        
    def initUI(self):

        self.speed = 0
        self.speedFade = 0
        global errorIconOn
        errorIconOn = 1
        #updateSerial().setSerialPort()    
        self.setupUpdateThread()  # thread
        #self.serialUpdateThread()  # thread
        
        self.setGeometry(300, 300, 800,300)  # window size
        self.show()
                        
    def paintEvent(self, event):
        
        if(self.speedFade == 0):
            self.speed = self.speed + 1
            if(self.speed >= 240):
                self.speedFade = 1
        else:
            self.speed = self.speed - 1
            if(self.speed <= 0 ):
                self.speedFade = 0
        
        
        qp = QtGui.QPainter(self)
        baseImage = QtGui.QImage("base.png")
        qp.drawImage(0,0,baseImage)
        qp.end()
        
        qtime = QtGui.QPainter(self)
        atime = QtCore.QTime.currentTime()
        qtime.setPen(QtGui.QColor(220, 220, 220))
        qtime.setFont(QtGui.QFont('Decorative', 10))
        qtime.drawText(QtCore.QRect(360,10,80,50),QtCore.Qt.AlignCenter,str(atime.hour()) + ":" + str(atime.minute()) + ":" + str(atime.second()))
        qtime.end()
        
        qspeed = QtGui.QPainter(self)
        qspeed.setPen(QtGui.QColor(220, 220, 220))
        qspeed.setFont(QtGui.QFont('LCDMono2', 40))
        qspeed.drawText(QtCore.QRect(339,105,120,55),QtCore.Qt.AlignCenter, str(self.speed))
        qspeed.end()
        
        qp2 = QtGui.QPainter(self)
        speedPointerImage = QtGui.QImage("speedPointer.png")
        qp2.translate(400,150)
        qp2.rotate(-222 + (int(self.speed)/1.081))
        qp2.drawImage(0,0,speedPointerImage)
        qp2.end()

        if (errorIconOn == 1):
            qp3 = QtGui.QPainter(self)
            errorIconImage = QtGui.QImage("errorIcon.png")
            qp3.drawImage(QtCore.QRect(160,100,50,50),errorIconImage)
            qp3.end()

        
        self.update()

    # update GUI current time label  
    def updateSpeed(self, text):
        self.speed = int(text)
        self.speedLabel.setText(str(text))

    # update GUI current time label
    def updateTime(self):
        time = QtCore.QTime.currentTime()
        self.timeLabel.setText(str(time.hour()) + ":" + str(time.minute()) + ":" + str(time.second())) 
            
    def setupUpdateThread(self):  
        self.updateThread = upateThread()  
        # connect our update functoin to the progress signal of the update thread  
        #self.updateThread.progress.connect(self.updateTime, QtCore.Qt.QueuedConnection)  
        #self.updateThread.progress.connect(self.updateSerial, QtCore.Qt.QueuedConnection)  
        if not self.updateThread.isRunning():  # if the thread has not been started let's kick it off  
            self.updateThread.start()     
    
    
    #def serialUpdateThread(self):  
    #    self.updateSerial = updateSerial()  
        # connect our update functoin to the progress signal of the update thread  
     #   self.updateSerial.progress.connect(self.updateSpeed, QtCore.Qt.QueuedConnection)
   #     #self.updateThread.progress.connect(self.updateSerial, QtCore.Qt.QueuedConnection)  
    #    if not self.updateSerial.isRunning():  # if the thread has not been started let's kick it off  
    #        self.updateSerial.start()     
                            
# inherit from Qthread and setup our own thread class  
class upateThread(QtCore.QThread):  
    progress = QtCore.Signal(str)  # create a custom sygnal we can subscribe to to emit update commands  
    def __init__(self, parent=None):  
        super(upateThread, self).__init__(parent)  
        self.exiting = False  
  
    def run(self):  
        while True:  
            self.msleep(10)
            self.progress.emit(str(random.randint(0, 280)))              

            
class canBusSetup:
    
    def setSerialPort(self):
        print("CANbus")       


class Central(QtGui.QWidget):
    
    def __init__(self):
        super(Central, self).__init__()
        
        self.initUI()
        
    def initUI(self):

      
        self.setGeometry(900, 300, 400,800)  # window size
        self.show()
            
def main():
    app = QtGui.QApplication(sys.argv)

    ex = Base()
    ex2 = Central()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()