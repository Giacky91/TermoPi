########################
#
#http://webshed.org/wiki/RaspberryPI_DS1820
#
#######################
#!/usr/bin/env python
import os
import glob
import time
import MySQLdb

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
_USER = 'sensor'
_PSWDB = 'senspsw'
_STATUS = 'ATT'
_DB = 'temperature'
_ADDR = 'localhost'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    #37 00 4b 46 ff ff 07 10 1e : crc=1e YES  - YES = temp readed
    #37 00 4b 46 ff ff 07 10 1e t=27312  -  t=value
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def write_temp_DB(temp):
    try:
        db = MySQLdb.connect(host = _ADDR, user = _USER, password = _PSWDB, database = _DB)
        curs = db.cursor();

        #curs.execute ("INSERT INTO tempdata (data, time, value, user_insert, status) VALUES(current_date(), now(), 21.0, 'sensor', 'ATT');")
        #db.commit()

        query = 'INSERT INTO temp_data (value, data, time, user_insert, status) VALUES({0}, current_date(), now(), {1}, {2} );'.format(temp, _USER, _STATUS)

        curs.execute(query)
        db.commit()
        db.close()
    except:
        print "Error: the database is being rolled back"
        db.rollback()
        db.close()

def startRead(interval):
    try:
        maxTime = interval * 60
        while True:
            #count the time to execute the while loop
            startTime = time.time()
            
            #print the temp
            temp = read_temp()
            #write_temp_DB(temp)
            #print(temp)
            
            #end execute
            endTime = time.time()
            #wait for freq value minus operation time
            time.sleep(maxTime - (endTime - startTime))
    except KeyboardInterrupt:
            print "Ctrl-C pressed\nStop reading the temperature..."
