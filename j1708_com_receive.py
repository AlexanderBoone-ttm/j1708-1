import serial, time, csv, sys, signal, os
from j1708 import Message,checksum



def signal_handler(signal, handler):
    if 'com' in globals():
        if com.is_open:
            com.close()
    print('Script interrupted!\n')
    log_file.close()
    if os.path.getsize(abs_file_path)==0:
        os.remove(abs_file_path)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def handle_data(data):
    timestamp = time.strftime("%d/%m %H:%M:%S",time.gmtime())
    data = [ord(i) for i in data]
    check = checksum(data)
    log_string = timestamp +' SUM: '+str(check)+'  \t'+ str(data)
    if check == data[-1]:
        log_string = 'STATUS_OK ' + log_string
    else:
        log_string = 'WRONG_SUM! ' + log_string
    #data = ord(data)
    log_file.write(log_string+'\n')
    print(log_string)
    parse_for_fuel(data)


def parse_for_fuel(array):
    if array[0] == 128:
        for i in range(0,(len(array)-1)):
            if (array[i] == 133): #avarage fuel rate L/s
                step = 16.428E-6
                dataH = array[i+1]
                dataL = array[i+2]
                data = (dataH<<8)|dataL
                print("Current fuel rate: ="+str(data)+"\n")
                break;       


com = serial.Serial()
com.port = "COM21"
com.baudrate = 9600
com.timeout= (1/9600)*22
com.STOPBITS = 1
com.PARITIES = 0
com.set_buffer_size = 21
com.interCharTimeout = 0.01

if ~com.is_open:
    com.open()

if not os.path.exists('logs'):
    os.makedirs('logs')

log_stamp = time.strftime("%d_%m_%H_%M_%S",time.gmtime())
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "logs/log_"+log_stamp+'.txt'
abs_file_path = os.path.join(script_dir, rel_path)
log_file = open(abs_file_path,'w')

while True:
    #print("test")
    if com.inWaiting():
        time.sleep(0.001) #0.005
        reading = com.readline()
        handle_data(reading)

#receiver's code

        



com.close()
