#!/usr/bin/env python3
"""
Stupid script to read a csv and dump it to a file.
Do not copy this because it's terrible and you can do better.

Love,
Owen
"""

import signal
import time
import sys
import csv
import datetime

def sigterm(sig, frame):
    print("SIGTERM. Quitting...")
    sys.exit(1)

signal.signal(signal.SIGINT, sigterm)

class Found(Exception):
    pass

class NotFound(Exception):
    pass

def get_data():
    with open('stats.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            yield row

def main():
    today = datetime.datetime.now().date()
    while True:
        time.sleep(2)
        try:
            with open("stats.txt", "r") as inf:
                prev = inf.read()

            data = list(get_data())
            for row in data[:len(data)-2:-1]: # first 2 are just labels
                row_date = datetime.datetime.strptime(row[0], "%m-%d-%Y").date()
                if(row_date == today):
                    L = 0
                    W = 0
                    ZvZ = f"ZvZ {row[1]} - {row[2]}\n"
                    W += int(row[1])
                    L += int(row[2])
                    ZvT = f"ZvT {row[3]} - {row[4]}\n"
                    W += int(row[3])
                    L += int(row[4])
                    ZvP = f"ZvP {row[5]} - {row[6]}\n"
                    W += int(row[5])
                    L += int(row[6])
                    All = f"All {W} - {L}\n"
                    Totes = f"Total {W+L}\n"
                    with open("stats.txt", "w") as outf:
                        outf.writelines(ZvZ)
                        outf.writelines(ZvT)
                        outf.writelines(ZvP)
                        outf.writelines(All)
                        outf.writelines(Totes)
                    raise Found()# if we find today we stop searching the rows
            # if we don't find today in the csv rows.
            raise NotFound()
        except Found:
            continue
        except NotFound:
            with open("stats.txt", "w") as outf:
                outf.writelines(f"No data for\n{today.strftime('%m-%d-%Y')}!\n")
        except (PermissionError, FileNotFoundError, ) as e:
            print(e)
            with open("stats.txt", "w") as outf:
                outf.write(prev)
            continue


if __name__ == "__main__":
    main()
