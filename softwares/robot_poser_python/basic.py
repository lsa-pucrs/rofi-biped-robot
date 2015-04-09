import serial
ser = serial.Serial('com7', 9600)

print ser.readline()
while(True):
    valor=int(raw_input("wait"))
    rh6=chr(valor)+chr(valor)
    rul5=chr(valor)+chr(valor)
    rml4=chr(valor)+chr(valor)
    rk3=chr(valor)+chr(valor)
    rll2=chr(valor)+chr(valor)
    ra1=chr(valor)+chr(valor)

    lh6=chr(valor)+chr(valor)
    lul5=chr(valor)+chr(valor)
    lml4=chr(valor)+chr(valor)
    lk3=chr(valor)+chr(valor)
    lll2=chr(valor)+chr(valor)
    la1=chr(valor)+chr(valor)
    
    mens='cmd'+rh6+rul5+rml4+rk3+rll2+ra1+lh6+lul5+lml4+lk3+lll2+la1
    #print ser.readline()
    print(mens)

    #ser.write('hi')
    
    ser.write('cmd')
