import sqlite3
import argparse


def dataCheck(name, hash, database):
    try:
        con = sqlite3.connect(database)
        cur = con.cursor()
        dbhash = cur.execute("SELECT hash FROM videos WHERE name=\"{}\"".format(name))
        hash2 = next(dbhash)
        con.close()
        if hash != hash2[0]:
            with open("corrupted-files.txt", "a") as f:
                f.write("file is corrupted: Filename = {}, primaryHash = {}, secondaryHash = {}\n".format(name, hash, hash2[0]))
            print("file is corrupted: Filename = {}, primaryHash = {}, secondaryHash = {}".format(name, hash, hash2[0]))
    except:
        print("file name is not present: Filename = {}".format(name))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This is for hashing files in a folder")
    parser.add_argument("-v","--version",action="version",version="%(prog)s v1.0")
    parser.add_argument("primaryDB",type=str,help="The primary Database with all the original hash")
    parser.add_argument("secondaryDB",type=str,help="The secondary Database with all the check hash")
    argv = parser.parse_args()
    con = sqlite3.connect(argv.primaryDB + ".sqlite3")
    cur = con.cursor()
    data = cur.execute("SELECT * from videos")
    for d in data:
        dataCheck(d[0], d[1], argv.secondaryDB + ".sqlite3")
    con.close()