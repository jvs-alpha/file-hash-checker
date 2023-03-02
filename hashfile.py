#!/usr/bin/python3
import os
import hashlib
import argparse
import sys
import sqlite3

def createDB(database):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("CREATE TABLE videos( name CHAR (100) PRIMARY KEY, hash CHAR (70) NOT NULL )")
    con.close()

def writeDB(database, name, hash):
    con = sqlite3.connect(database)
    cur = con.cursor()
    val = "INSERT INTO videos VALUES (\"{}\", \"{}\")".format(name,hash)
    cur.execute(val)
    con.commit()
    con.close()


def HashSHA256(folder, db):
    files = os.listdir(folder)
    for f in files:
        filename = f
        f = os.path.join(folder,f)
        if os.path.isdir(f):
            HashSHA256(f, db)
            continue
        try:
            with open(f,"rb") as fd:
                fdata = fd.read()
            hash = hashlib.sha256(fdata).hexdigest()
            writeDB(db, filename, hash)
            print("{} - {}".format(f,hash))
        except KeyboardInterrupt:
            sys.exit()
        except:
            with open("NotHashedFiles-{}.txt".format(db), "a") as d:
                d.write("File can not be hashed - {}\n".format(f))
            print("File can not be hashed - {}".format(f))


if __name__  ==  "__main__":
    parser = argparse.ArgumentParser(description="This is for hashing files in a folder")
    parser.add_argument("-v","--version",action="version",version="%(prog)s v1.0")
    parser.add_argument("Folder",type=str,help="This is the folder of files to be hashed")
    parser.add_argument("Database",type=str,help="This is the DB with the hash values. Enter name without sqlite3 extension")
    argv = parser.parse_args()
    createDB(argv.Database + ".sqlite3")
    HashSHA256(argv.Folder, argv.Database + ".sqlite3")
