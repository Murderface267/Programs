
import time, os

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
        def readadc(self,adcnum, clockpin, mosipin, misopin, cspin):
                if ((adcnum > 7) or (adcnum < 0)):
                        return -1
                GPIO.output(cspin, True)

                GPIO.output(clockpin, False)  # start clock low
                GPIO.output(cspin, False)     # bring CS low

                commandout = adcnum
                commandout |= 0x18  # start bit + single-ended bit
                commandout <<= 3    # we only need to send 5 bits here
                for i in range(5):
                        if (commandout & 0x80):
                                GPIO.output(mosipin, True)
                        else:
                                GPIO.output(mosipin, False)
                        commandout <<= 1
                        GPIO.output(clockpin, True)
                        GPIO.output(clockpin, False)

                adcout = 0
                # read in one empty bit, one null bit and 10 ADC bits
                for i in range(12):
                        GPIO.output(clockpin, True)
                        GPIO.output(clockpin, False)
                        adcout <<= 1
                        if (GPIO.input(misopin)):
                                adcout |= 0x1

                GPIO.output(cspin, True)

                adcout >>= 1       # first bit is 'null' so drop it
return adcout

def send_HID(HID_String):
    os.system('echo -ne "' + HID_String + '" > /dev/hidg0')
def send_HID_Bash():
    os.system('test.bsh')
threshold = 20
PC_locked = False
fp = open('config.txt','r')
sleep_time = int(fp.read().strip())
fp.close()
while 1:
    do_HID = False
    sensor_value = adcout()
    if sensor_value < threshold and not PC_locked:
        do_HID = True
    else:
        do_HID = False
        PC_locked = False
        time.sleep(1)
    if do_HID:
        time.sleep(sleep_time)
        sensor_value = adcout()
        if sensor_value < threshold:
            send_HID_Bash()
            PC_locked = True
        else:
            do_HID = False
