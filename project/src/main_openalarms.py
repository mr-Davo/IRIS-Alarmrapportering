import os
import calendar
import os.path
import sys
from time import time
from datetime import datetime

from UploadFile import UploadFile
from StatisticalReport import CreateOpenAlarmsFile
import TerugkoppelingExcelFile
import OpenAlarmsExcelFile
from Merge import Load, Save

def OpenAlarms(Log,key):
    FolderName = "IRIS"
    DriveID = '1BcCQCnQ8No47ZB0oixKW9m4Ye2pU9eL_'
    #FolderName = "test"
    #DriveID = '0AIm6EsRAnC2mUk9PVA'

    csv_file =  CreateOpenAlarmsFile(Log)

    print("Creating Excel file for Actual Alarms")
    file = OpenAlarmsExcelFile.CreateExcelFile(csv_file)

    open_alarms_file_name = {'open_alarms': "Openstaande Alarmen"}
    Save(open_alarms_file_name, "dates.json")

    feedback = UploadFile(file, FolderName, DriveID,key , FileName = open_alarms_file_name['open_alarms'])
    os.remove(file)
    os.remove(csv_file)

    return feedback

def main():
    paths_dic = Load("source_paths.json")
    start_time = time()
    ActueelAlarms = paths_dic["open_alarms_log"]

    

    if os.path.exists(ActueelAlarms):
        Feedback = OpenAlarms(ActueelAlarms, 'open_alarms')
    print("")
    
    os.remove(ActueelAlarms)
    
if __name__ == '__main__':
    print("Starting")
    sys.exit(main())