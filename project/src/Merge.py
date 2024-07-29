import os.path
import pandas as pd
from datetime import datetime
import json

def Save(variables, filename):
    #Set working directory to data folder
    os.chdir(os.path.join(os.getcwd(),"data"))

    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        # Load the data from the JSON file
        with open(filename, 'r') as file:
            data = json.load(file)    
        for key in variables.keys():
                data[key] = variables[key]
    else:
        data = variables

    """Save multiple variables to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    os.chdir(os.path.dirname(os.getcwd()))

def Load(filename):
    #Set working directory to data folder
    os.chdir(os.path.join(os.getcwd(),"data"))
    
    """Load multiple variables from a JSON file."""
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as file:
            try:
                variables = json.load(file)
            except json.JSONDecodeError:
                variables = {}  # Return an empty dictionary if the JSON is malformed
    else:
        variables = {}  # Return an empty dictionary if the file does not exist or is empty
    os.chdir(os.path.dirname(os.getcwd()))
    return variables

def CreateHistory(csv_file, save_path):
    week_name = GenerateFileName(week=True)
    logW = os.path.join(save_path, week_name)

    if not os.path.exists(logW):
        # Create the week log if new week
        with open(logW, "w") as file:
            pass
    
    MergeCSV(logW, csv_file,week_name)

    month_name = GenerateFileName(week=False)
    logM = os.path.join(save_path, month_name)

    if not os.path.exists(logM):
        # Create the month log if new month
        with open(logM, "w") as file:
            pass

    file_name_json='dates.json'
    
    MergeCSV(logM, csv_file,month_name)

    new_files = {
    "week": week_name,
    "month": month_name,
    }

    old_files = Load(file_name_json)
    os.chdir(os.path.join(os.getcwd(),"data"))
    if os.path.exists(file_name_json):
        for key in ["week", "month"]:
            if key in old_files:
                if old_files[key] != new_files[key]:
                    os.remove(os.path.join(save_path,old_files[key]))
    os.chdir(os.path.dirname(os.getcwd()))

    Save(new_files,file_name_json)
    

    
    Logs = [logW,logM]
    return Logs


def GenerateFileName(week):
    if week:
        date_str = datetime.now().strftime('w%W')
    else:
        date_str = datetime.now().strftime('%Y-%m')
    name = f'{date_str}_Alarmrapport.csv'
    return name

def MergeCSV(log, csvfile1,NameCSV):
       
    # Read the first CSV file
    df1 = pd.read_csv(csvfile1, sep =";")
    
    if os.path.getsize(log) != 0:
        # Read the second CSV file
        df2 = pd.read_csv(log, sep =",")
        total_df = pd.concat([df2, df1], ignore_index=False)
    else:
        total_df = df1

    total_df.to_csv(log, sep=',', index=False)
    Name = os.path.basename(log)


