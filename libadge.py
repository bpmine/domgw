import serial
import serial.tools.list_ports
import time
from threading import Thread
import re;



class BadgeReader(Thread):
    port=None
    ser=None
    cbs=set()
    def setRedLed(self,state):
        if (state==True):
            self.ser.write(b"ledron\n")
        else:
            self.ser.write(b"ledroff\n")
            
        resp=self.ser.readline()

    def setGreenLed(self,state):
        if (state==True):
            self.ser.write(b"ledvon\n")
        else:
            self.ser.write(b"ledvoff\n")
            
        resp=self.ser.readline()
    
    def __init__(self,port):
        self.port=port
        self.ser=serial.Serial(port,9600,timeout=8,parity=serial.PARITY_NONE)
        time.sleep(2)
        Thread.__init__(self)
                
    def test(self):
        self.setRedLed(True)
        self.setGreenLed(True)

        time.sleep(1)

        self.setRedLed(True)
        self.setGreenLed(False)

        time.sleep(1)
        
        self.setRedLed(False)
        self.setGreenLed(True)

        time.sleep(1)

        self.setRedLed(False)
        self.setGreenLed(False)

    def close(self):
        self.ser.close()

    def addListener(self,cb):
                self.cbs.add(cb)

    def run(self):
        p=re.compile("^carte=(.+)");
        
        while True:
                lut=self.ser.readline();
                if (lut==b'') or (lut==b'\r\n'):
                        continue

                chaineLue=lut.decode("UTF8").strip();
                m=p.match(chaineLue)
                if (m!=None):
                        id=m.group(1)
                        for cb in self.cbs:
                                cb(self,id)
                        

def carteRecue(rdr,chaine):
        print(chaine)

def main():
        r=BadgeReader("COM3")
        r.addListener(carteRecue)
        r.test()
        r.start()


if __name__ == "__main__":
        main()



