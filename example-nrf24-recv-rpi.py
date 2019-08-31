#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example program to receive packets from the radio link
#

import spidev
import time
from lib_nrf24 import NRF24
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio2 = NRF24(GPIO, spidev.SpiDev())
radio2.begin(0, 17)

radio2.setRetries(15, 15)

radio2.setPayloadSize(32)
radio2.setChannel(0x60)
radio2.setDataRate(NRF24.BR_2MBPS)
radio2.setPALevel(NRF24.PA_MIN)

radio2.setAutoAck(True)
radio2.enableDynamicPayloads()
radio2.enableAckPayload()

radio2.openWritingPipe(pipes[0])
radio2.openReadingPipe(1, pipes[1])

radio2.startListening()
radio2.stopListening()

radio2.printDetails()

radio2.startListening()

c = 1

try:
    while True:
        akpl_buf = [c, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8]
        pipe = [0]
        while not radio2.available(pipe):
            time.sleep(10000/1000000.0)

        recv_buffer = []
        radio2.read(recv_buffer, radio2.getDynamicPayloadSize())
        print("Received:"),
        print(recv_buffer)
        c = c + 1
        if (c & 1) == 0:
            radio2.writeAckPayload(1, akpl_buf, len(akpl_buf))
            print("Loaded payload reply:"),
            print(akpl_buf)
        else:
            print("(No return payload)")

except KeyboardInterrupt:
    # here you put any code you want to run before the program
    # exits when you press CTRL+C
    print("\n")  # print value of counter
except:
    # this catches ALL other exceptions including errors.
    # You won't get any error messages for debugging
    # so only use it once your code is working
    print("Other error or exception occurred!")

finally:
    GPIO.cleanup()  # this ensures a clean exit
