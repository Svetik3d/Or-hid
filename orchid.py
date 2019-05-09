#!/usr/bin/env python
# -*-coding: utf-8 -*-
# vim: sw=4 ts=4 expandtab ai

import time
import datetime
import termios
import socket
import serial


PORT = '/dev/ttyACM0'
PORT_SPEED = 9600
PATH = "/home/sveta/cnf.txt"


def main():
    # Fix arduino reset on serial connect by disabling DTS
    # stty -F /dev/ttyUSB0 -hupcl
    # See http://atroshin.ru/ru/content/
    #  avtomaticheskaya-perezagruzka-arduino-pri-podklyuchenii-terminala
    with open(PORT) as port:
        attrs = termios.tcgetattr(port)
        attrs[2] = attrs[2] & ~termios.HUPCL
        termios.tcsetattr(port, termios.TCSAFLUSH, attrs)
    ser = serial.Serial(PORT, PORT_SPEED, timeout=1)
    time.sleep(0.5)
    received = []
    #"H" - влажность
    #"T" - температура с большого датчика
    #"1" - включить свет
    #"t" - температура с маленького датчика
    #"2" - выключить свет
    time.sleep(5)
    whi = True
    now = datetime.datetime.now()
    with open(PATH, "r") as files:
        time_on, time_off = files.read().split("\n")
        time_on_h, time_on_m = time_on.split(":")
        time_off_h, time_off_m = time_off.split(":")
        time_on = now.replace(hour=int(time_on_h), minute=int(time_on_m), second=0, microsecond=0)
        time_off = now.replace(hour=int(time_off_h), minute=int(time_off_m), second=0, microsecond=0)
    if time_off >= now >= time_on:
        ser.write("1")
    else: 
        ser.write("2")
    ser.write("t")
    ser.write("T")
    ser.write("H")
    akk = 0
    while whi:
        line = ser.readline()
        if line:
            received.append(line.decode().strip())
            akk = akk+1
            if akk == 3:
                whi = False
    sock = socket.socket()
    sock.connect(('192.168.0.1', 2003))
    untime = time.time()
    sock.send("orchid.temp_1 " + str(received[0]) + " " + str(untime) + "\n")
    sock.send("orchid.temp_2 " + str(received[1]) + " " + str(untime) + "\n")
    sock.send("orchid.humidity " + str(received[2]) + " " + str(untime) + "\n")

if __name__ == '__main__':
    main()
