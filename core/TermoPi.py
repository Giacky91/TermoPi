##############################################
#                                            #
#                TermoPi                     #
#                 v 0.1                      #
#                                            #
##############################################
#!/usr/bin/env python
#TODO:
#    + set-up DB connection
#    + works with only 1 option/argument( -f/--freq)
#    - create log file
#    - run readTemp.py(testTemp.py) script OR add thread to run readTemp.py
#    - blank file to check if TermoPi is running checking at startup

#__doc__
"""
termo.py -p/--freqprog <frequency> -t/--freqtemp <frequency> | -h/--help | -v/--version
   -h, --help:     show this message
   -p, --freqprog: set the frequence in minutes to check the setted temperature( Default: 5)
   -t, --freqtemp: set the frequence in minutes to read the temperature from sensor( Default: 10)
   -v, --version:  version
"""

#Imports
import readTemp
import sys
import getopt
import time
import MySQLdb

#Constats
_STDFREQUSR = 5
_STDFREQTMP = 10
_VERSION = 0.1
_USER = 'core'
_PSWDB = 'corepsw'
_DB = 'temperature'
_ADDR = 'localhost'
_RELAY_PIN = 12 #insert correct pin value

#Global
#db = MySQLdb.connect(_ADDR, _USER, _PSWDB, _DB)

def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:vt:', ['help', 'freqprog=', 'version', 'freqtemp='])
    except getopt.error, msg:
        print msg
        print 'for help use --help'
        sys.exit(2)
    # process options
    for key, value in opts:
        if key in ('-h', '--help'):
            print __doc__
            sys.exit(0)
        if key in ('-v', '--version'):
            print 'TermoPi.py\nVersion ' + str(_VERSION)
            sys.exit(0)
        if key in ('-p', '--freqprog'):
            _STDFREQUSR = value
        if key in ('-t', '--freqtemp'):
            _STDFREQTMP = value
    startTermo()

def startTermo():
    relayOn = False
    try:
        maxTime = _STDFREQUSR * 60
        GPIOsetup()
        while True:
            #count the time to execute the while loop
            startTime = time.time()
            #setDBConn()
            
            curs = db.cursor();
            #read the current temp
            query = 'SELECT VALUE FROM TEMP_DATA ORDER BY DATA DESC, TIME DESC;'
            curs.execute(query)
            lastReadTemp = float(curs.fetchone())
            
            #read the temp setted by user
            query = 'SELECT SET_VALUE FROM USR_TEMP_DATA ORDER BY DATA DESC, TIME DESC;'
            curs.execute(query)
            userSetTemp = float(curs.fetchone())
            #then do stuff
            
            if lastReadTemp < userSetTemp:
                #if relayOn == True, relay is alrady working
                if relayOn == False:
                    #azione il rele
                    GPIO.output(FAN_PIN, GPIO.HIGH)
                    relayOn = True
            elif relayOn == True:
                #spengo il rele
                GPIO.output(FAN_PIN, GPIO.LOW)
                relayOn = False
            
            db.close()
            #end execute
            endTime = time.time()
            
            #wait for freq value minus operation time
            time.sleep(maxTime - (endTime - startTime))
    except KeyboardInterrupt:
        print 'Ctrl-C: close the script'
    except:
        print 'Error: the database is being rolled back'
        db.rollback()
        db.close()
    finally:
        db.close()
        
#Database Connection
def setDBConn():
    global db 
    db = MySQLdb.connect(_ADDR, _USER, _PSWDB, _DB)
    curs = db.cursor();
    
#set up GPIO pin
def GPIOsetup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(FAN_PIN, GPIO.OUT)

#Main
if __name__ == '__main__':
    main()
