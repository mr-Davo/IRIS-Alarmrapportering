import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from tqdm import tqdm
import re

def CreateReportFile(IRIS_log,**kwargs):
    # Filter logbook to the necessary Priority labels
    total_df = pd.read_csv(IRIS_log, sep =",")
    
    if 'Dag' in kwargs:
        zichtbaar =  ["Niet dringend VTC", "Niet dringend VTC Vertraagd", "Beperkt dringend VTC", "Beperkt dringend VTC Vertraagd", "Ernstig VTC", "Ernstig VTC Vertraagd", "Kritisch VTC", "Kritisch VTC Vertraagd", "Melding VTC", "Fout VTC"]
        #zichtbaar = ["Gevaar VVC", "Nood VVC"]
        df = total_df[total_df.iloc[:,1].isin(zichtbaar)]

        # Generate a list from all the columns in the csv file
        Groep = df.iloc[:,1]
        Berichten = df.iloc[:, 2]
        Begintijd = ReformatDate(df.iloc[:,4]) 
        Eindtijd = ReformatDate(df.iloc[:,5])   
        Bevestigd = ReformatDate(df.iloc[:,6])
        
        # Calculate the duration of the alarms that are finished
        ## Convert to pandas datetime, handling empty strings
        Eindtijd = pd.to_datetime(Eindtijd)
        Begintijd = pd.to_datetime(Begintijd)

        ## Calculate the duration
        Duur_timedelta = Eindtijd - Begintijd

        ## Convert to total seconds, handle NaT (Not a Time) separately
        Duur_seconds = Duur_timedelta.total_seconds()

        Duur = ["" if pd.isna(duration) else int(duration) for duration in Duur_seconds]
        
        # Generate the Log.csv file
        Log = {'Groep': Groep,
            'Berichten': Berichten,
            'Begintijd': Begintijd,
            'Eindtijd': Eindtijd,
            'Duur': Duur,
            'Bevestigd': Bevestigd,
            'Bevestigd Door': df.iloc[:,7]
        }
        Logboek = pd.DataFrame(Log)
        Logboek.to_csv("Log.csv", index = False, sep=';')

        # Generate the Logbook.csv file
        Log = {'Groep': Groep,
            'Berichten': Berichten,
            'Begintijd': Begintijd,
            'Eindtijd': Eindtijd,
            'Duur': FormatDuur(Duur),
            'Bevestigd': Bevestigd,
            'Bevestigd Door': df.iloc[:,7]
        }
        Logboek = pd.DataFrame(Log)

        
    else:
        Groep = total_df["Groep"]
        Berichten = total_df["Berichten"]
        Begintijd = total_df["Begintijd"]
        Eindtijd = total_df['Eindtijd']
        Duur_seconds = total_df['Duur']
        Bevestigd = total_df['Bevestigd']
        BevestigdDoor = total_df['Bevestigd Door']

        Duur = ["" if pd.isna(duration) else int(duration) for duration in Duur_seconds]

        Log = {'Groep': Groep,
            'Berichten': Berichten,
            'Begintijd': Begintijd,
            'Eindtijd': Eindtijd,
            'Duur': FormatDuur(Duur),
            'Bevestigd': Bevestigd,
            'Bevestigd Door': BevestigdDoor
        }
        
    Logboek = pd.DataFrame(Log)
    print("Logboek klaar")
    Logboek.to_csv("Logboek.csv", index = False, sep=';')

    Alarmlijst = np.unique(Berichten)
    # initialize the other columns of the Rapport
    Aantal = np.zeros(len(Alarmlijst))
    Gem_Duur = np.empty(len(Alarmlijst), dtype=object) 
    Min_Duur = np.empty(len(Alarmlijst), dtype=object) 
    Max_Duur = np.empty(len(Alarmlijst), dtype=object) 
    Prio = np.empty(len(Alarmlijst), dtype=object)  

    # Creating a dictionary for faster lookup of priorities
    priority_dict = dict(zip(Berichten, Groep))

    # Get the values of the columns: Aantal, Gem_Duur, Min_Duur, Max_Duur, Prio
    for i, Alarm in enumerate(tqdm(Alarmlijst, desc="Processing Alarms")):
        total, gemd, mind, maxd = CalculateStatistics(Alarm, Berichten, Duur)
        Aantal[i] = total
        Gem_Duur[i] = gemd
        Min_Duur[i] = mind
        Max_Duur[i] = maxd
        # Get the priority group of the first occurrence of the alarm
        Prio[i] = priority_dict[Alarm]
    
    # Split the Alarm message
    Alarmen = SplitBoodschap(Alarmlijst)

    # Generate the Rapport.csv file
    Log = {'Groep': Prio,
            'Tunnel': Alarmen[0],
            'Techniek': Alarmen[1],
            'Richting': Alarmen[3],
            'Alarm Boodschap': Alarmen[2],
            'Aantal': Aantal,
            'Gem Duur': FormatDuur(Gem_Duur),
            'Max Duur': FormatDuur(Max_Duur),
            'Min Duur': FormatDuur(Min_Duur)
    }
    print("Rapport klaar")
    Logboek = pd.DataFrame(Log)
    Logboek.to_csv("Rapport.csv", index = False, sep=';')
    if 'Dag' in kwargs:
        csv_files = ["Logboek.csv","Rapport.csv","Log.csv"]
        return csv_files
    else: 
        csv_files = ["Logboek.csv","Rapport.csv"]
        return csv_files

def CreateOpenAlarmsFile(Log):
    # Filter logbook to the necessary Priority labels
    total_df = pd.read_csv(Log, sep =",")
    #zichtbaar =  ["Niet dringend VTC", "Niet dringend VTC Vertraagd", "Beperkt dringend VTC", "Beperkt dringend VTC Vertraagd", "Ernstig VTC", "Ernstig VTC Vertraagd", "Kritisch VTC", "Kritisch VTC Vertraagd", "Melding VTC", "Fout VTC"]
    #df = total_df[total_df.iloc[:,7].isin(zichtbaar)]

    df = total_df[total_df['OffTime'].isna()]

    # Generate a list from all the columns in the csv file
    Berichten = df.iloc[:,0]
    Begintijd = ReformatDate(df.iloc[:, 2])
    Bevestigd = ReformatDate(df.iloc[:,5]) 
    BevestigdDoor = df.iloc[:,6]
    Groep = df.iloc[:,7]


    # Split the Alarm message
    Alarmen = SplitBoodschap(Berichten)

    Rapport = {'Groep': Groep,
            'Tunnel': Alarmen[0],
            'Techniek': Alarmen[1],
            'Richting': Alarmen[3],
            'Alarm Boodschap': Alarmen[2],
            'Aanvangstijd': Begintijd,
            'Tijd bevestigd': Bevestigd,
            'Bevestigd Door': BevestigdDoor
    }
    print("Openstaande Alarmen rapport klaar")
    Logboek = pd.DataFrame(Rapport)
    csv_file = "OpenAlarms.csv"
    Logboek.to_csv(csv_file, index = False, sep=';')

    return csv_file

def CalculateStatistics(Alarm, Berichten, Duur):
    aantal = 0
    td = timedelta(seconds=0)
    
    # Convert Duur to a numpy array for easier manipulation
    Duur = np.array(Duur)
    
    # Filter out empty strings from Duur and convert to float
    numeric_durations = np.where(Duur != "", Duur , np.nan)
    
    # Mask to filter out the elements where Berichten matches Alarm
    mask = Berichten == Alarm
    # Apply the mask to numeric_durations
    filtered_durations = np.array(numeric_durations[mask].astype(float))
    
    # Count the number of matches
    aantal = np.sum(mask)
    
    if all(np.isnan(x) for x in filtered_durations):
        mind = ""
        maxd = ""
        td = ""
        gd = ""
    else:
        # Calculate min, max, and total duration
        mind = int(np.nanmin(filtered_durations))
        maxd = int(np.nanmax(filtered_durations))
        td = int(np.nansum(filtered_durations))
        
        # Calculate average duration
        gd = td / aantal
    
    return aantal, gd, mind, maxd
 

def FormatDuur(array):
    # Initialize an empty list to store formatted strings
        Duur_str = []

        # Iterate over the array
        for duur in array:
            if duur != "":
                total_seconds = int(duur)
                days, rem = divmod(total_seconds,86400)
                hours, rem = divmod(rem, 3600)
                minutes, seconds = divmod(rem, 60)

                # Format seconds and minutes to always have two digits
                seconds = f"{seconds:02}"
                minutes = f"{minutes:02}"

                # Format the duration string based on the number of days
                if days >= 1:
                    duur_str = f"{days}d {hours}:{minutes}:{seconds}"
                else:
                    duur_str = f"{hours}:{minutes}:{seconds}"
            else:
                duur_str = ""
            # Append the formatted string to the list
            Duur_str.append(duur_str)

        # Convert the list to a NumPy array before returning
        return np.array(Duur_str)

def SplitBoodschap(Alarmlijst):
    Tunnel = []
    Richting = []
    Techniek = []
    Boodschap = []

    for alarm in Alarmlijst:
        try:
            arr = alarm.split(" - ")
            arr_len = len(arr)

            # Using list comprehension to extract elements
            Tunnel.append(arr[0] if arr_len >= 2 else None)
            Techniek.append(arr[1] if arr_len >= 3 else None)
            Richting.append(arr[2] if arr_len >= 4 else None)
            Boodschap.append(arr[-1])
        except Exception as e:
            print("Alarm: ", alarm)
            print("The error is: ",e)
            sys.exit()
    return Tunnel, Techniek, Boodschap, Richting

def ReformatDate(date_strings):
    reformatted_dates = []
    for date in date_strings:
        date_string = str(date)
        try:
            if date_string =='nan':
                reformatted_date_string = ""
            else:
                if CheckDatetimeFormat(date_string, '%m/%d/%Y %I:%M:%S %p %z'): 
                    # Preprocess the date string to remove the colon in the timezone offset
                    # Use regex to match the pattern and replace colon with empty string
                    date_string_processed = re.sub(r'(\+\d{2}):(\d{2})', r'\1\2', date_string)
                    
                    # Parsing the date string into a datetime object
                    date_object = datetime.strptime(date_string_processed, '%m/%d/%Y %H:%M:%S %p %z')
                    
                    # Formatting the datetime object to the desired format without timezone info
                    reformatted_date_string = date_object.strftime(' %Y/%m/%d %H:%M:%S')

                else:
                    reformatted_date_string = date_string
            reformatted_dates.append(reformatted_date_string)
        except Exception as e:
            print(e)
            print(date)
            print(len(reformatted_dates))
            sys.exit(0)
    
    return reformatted_dates

def CheckDatetimeFormat(date_string, format):
    try:
        # Attempt to parse the date_string with the specified format
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        # If parsing fails, it's not in the correct format
        return False