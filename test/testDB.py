#!/usr/bin/env python

import MySQLdb

db = MySQLdb.connect("localhost","root","Milano32","temperature")

#curs = db.cursor();

def write_to_DB():
    # note that I'm using triplle quotes for formatting purposes
    # you can use one set of double quotes if you put the whole string on one line
    curs = db.cursor();
    try:
        print "...start writing..."
        curs = db.cursor();
        print "insert..."
        curs.execute ("INSERT INTO tempdata (data, time, value, user_insert, status) VALUES(current_date(), now(), 21.0, 'sensor', 'ATT');")

        db.commit()
#        db.close()
        print "Data committed"

    except:
        print "Error: the database is being rolled back"
        db.rollback()
        db.close()

def read_from_db():
    curs = db.cursor();

    curs.execute ("SELECT * FROM tempdata;")
    print "\nDate            Time           Temperature"
    print "============================================"

    for reading in curs.fetchall():
         print str(reading[1])+"    "+str(reading[2])+"        "+str(reading[3])
    db.close()

def main():
    curs = db.cursor();
    print "cursor created..."
    write_to_DB()
    print "write data..."
    print "reading data..."
    read_from_db()

if __name__ == '__main__':
    main()
