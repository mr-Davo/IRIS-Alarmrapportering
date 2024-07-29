import os
import calendar
import os.path
import sys
from time import time
from datetime import datetime

from UploadFile_test import UploadFile
from StatisticalReport_test import CreateReportFile, CreateOpenAlarmsFile
import TerugkoppelingExcelFile_test
import OpenAlarmsExcelFile_test

def Terugkoppeling(IRIS_log):
    FolderName = "Andere Raporten"
    DriveID = '0AIm6EsRAnC2mUk9PVA'

    csv_files = CreateReportFile(IRIS_log)

    print("Creating Excel file for Terugkoppeling")
    file = TerugkoppelingExcelFile_test.CreateExcelFile(csv_files)
    for f in csv_files:
        os.remove(f)

    feedback = UploadFile(file,FolderName,DriveID)
    os.remove(file)

    return feedback

def OpenAlarms(Log):
    FolderName = "test"
    DriveID = '0AIm6EsRAnC2mUk9PVA'

    csv_file =  CreateOpenAlarmsFile(Log)

    print("Creating Excel file for Actual Alarms")
    file = OpenAlarmsExcelFile_test.CreateExcelFile(csv_file)

    feedback = UploadFile(file,FolderName,DriveID, FileName = "Openstaande Alarmen")
    os.remove(file)
    os.remove(csv_file)

    return feedback

def main():
    log_with_string= input(" Enter a path: ")
    #log = log_with_string.split('"')[1]
    log = r"C:\Users\daana\docs\werk\AWV\IRIS-alarmrapportering\Logs\w30_Alarmrapport.csv"
    print(log)
    #selec = input("Log or Open Alarms: ")
    selec = 'Log'

    while True:  
        if selec == 'Log':
            if os.path.exists(log):
                Feedback = Terugkoppeling(log)
            else:
                Feedback = "The log path does not exist."
                print(Feedback)
            break
        
        elif selec == 'open Alarms':
            if os.path.exists(log):
                Feedback = OpenAlarms(log)
            else:
                Feedback = "The open alarms path does not exist."
                print(Feedback)
            break
        else:
            selec = input("Log or Open Alarms: ")

    
if __name__ == '__main__':
    print("Starting")
    sys.exit(main())