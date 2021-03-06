#import the modules
from time import sleep
from logging.handlers import SysLogHandler
import syslog
from datetime import datetime
import sys
import csv
import logging
import random
from server import SyslogServer
import os

class ReadCSVFiles(object):
    def __init__(self, testEnabled=False):
        self.testEnabled = testEnabled

    #function that ships messages over the network
    def logMessages(self, logData):
        sysLogMessage = ''
        logData['Date Time'] = datetime.strptime(logData['Date Time'], '%Y-%m-%d %H:%M:%S')
        if self.testEnabled:
            if(logData['Login_Status'] == 'TRUE' or logData['Login_Status'] == 'True'):
                sysLogMessage = "sshd[%d]: Accepted publickey for %s from %s port %d ssh2 DATE_TIME %s HOST %s" %(random.randrange(1000, 9999, 345),logData['User'],logData['IP'],random.randrange(1021, 9999, 123),logData['Date Time'],logData['Server_Name'])
            else:
                sysLogMessage = "sshd[%d]: pam_unix(sshd:auth): authentication failure; login= uid=0 euid=0 tty=ssh ruser= rhost=%s user=%s DATE_TIME %s HOST %s" %(random.randrange(1000, 9999, 345),logData['IP'],logData['User'],logData['Date Time'],logData['Server_Name'])
        else:
            if(logData['Login_Status'] == 'TRUE' or logData['Login_Status'] == 'True'):
                sysLogMessage = "sshd[%d]: Accepted publickey for %s from %s port %d ssh2" %(random.randrange(1000, 9999, 345),logData['User'],logData['IP'],random.randrange(1021, 9999, 123))
            else:
                sysLogMessage = "sshd[%d]: pam_unix(sshd:auth): authentication failure; login= uid=0 euid=0 tty=ssh ruser= rhost=%s user=%s" %(random.randrange(1000, 9999, 345),logData['IP'],logData['User'])

        #log the message in syslogs
        logger.info(sysLogMessage)

    #this function reads each log from the csv
    #forms a dictionary with appropriate values
    #calls a function logMessages that forms the log messages based on success or failure
    def readLineGenerateLogs(self, reader):
        #the outer for loop generates the headers and inner for loop associates the values to headers
        rowNum = 0
        for row in reader:
            eachRowData = {}
            # Save header row.
            if rowNum == 0:
                fileData = row

            else:
                colNum = 0
                for col in row:
                    eachRowData[fileData[colNum]] = col
                    colNum += 1
                if(rowNum % 5 == 0):
                    sleep (50.0 / 1000.0)
                self.logMessages(eachRowData)
            rowNum += 1

#main function
def main():

    server = SyslogServer()
    server.parceConfig("../conf/server.conf")
    if server.testEnabled:
        #initiate an object for the class
        readCSV = ReadCSVFiles(server.testEnabled)
    else:
        readCSV = ReadCSVFiles()

    #initialize variables based on commandlines or defaults
    if len(sys.argv) >= 3:
        fileName = sys.argv[1]
        ipAddress = sys.argv[2]
    else:
        fileName = "data"
        ipAddress = "127.0.0.1"

    #these statements set up the syslog handler
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(address=(ipAddress, 10514))
    logger.addHandler(handler)

    #open file and generate a reader for csv files and close file
    fileObject  = open(fileName, "rb")
    reader = csv.reader(fileObject)

    #makes call to function that generates logs
    readCSV.readLineGenerateLogs(reader)
    fileObject.close()

if __name__ == "__main__":
  main()


