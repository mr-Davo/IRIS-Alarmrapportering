# IRIS Alarmrapportering

Dit Python-project leest dagelijks het IRIS logboek in CSV-formaat, genereert een Excel-rapport bestaande uit twee tabbladen (Logboek en Rapport), en slaat dit op in een gedeelde drive. Het project maakt hier dagelijks een rapport van en biedt een statistische verwerking van de gegevens in het logboek, inclusief het aantal keer dat een alarm is voorgevallen, de gemiddelde tijd, maximum- en minimumtijd. Deze dagelijske rapporten worden bijgeouden in de wekelijkse wekelijkse en maandelijkse rapporten om een gemakkelijk overzicht te beiden aan de gebruikers. Om de gebruikers een volledig beeld te geven van de situatie genereert het script ook een log met alle opstaande alarmen.

## Inhoud

- [Functies](#functies)
- [Installatie](#installatie)
- [Mappenstructuur](#Mappenstructuur)
- [Gebruik](#gebruik)
- [Code](#Code)
- [Licentie](#licentie)

## Functies

- **Inlezen van een CSV-logboek**: Leest het logboek in CSV-formaat.
- **Genereren van een Excel-rapport**: Maakt een Excel-bestand met twee tabbladen: Logboek en Rapport.
- **Statistische verwerking**: Bereken het aantal voorvallen, de gemiddelde tijd, de maximale en minimale tijd van de alarmen.
- **Opslaan op gedeelde drive**: Slaat het gegenereerde rapport op in een gedeelde drive VVC_VTC Rapporten.
- **Wekelijkse en maandelijkse rapporten**: Genereert en uploadt wekelijkse en maandelijkse rapporten voor overzicht en analyse.
- **Verwerken van opstaande alarmen**: Verwerkt een log van alle opstaande alarmen tot een Excel-document.

## Installatie

Om dit project lokaal te installeren, volgt u deze stappen:

1. Clone de repository:
    ```bash
    git clone https://github.com/mr-Davo/IRIS-alarmrapportering.git
    ```
2. Navigeer naar de projectmap:
    ```bash
    cd IRIS-alarmrapportering
    ```
3. Maak een virtuele omgeving aan:
    ```bash
    python -m venv env
    ```
4. Activeer de virtuele omgeving:
    - Op Windows:
        ```bash
        .\env\Scripts\activate
        ```
    - Op macOS en Linux:
        ```bash
        source env/bin/activate
        ```
5. Installeer de vereiste dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Mappenstructuur

Onderstaand een voorbeeld van de mappenstructuur wanneer het project actief is.

    IRIS-alarmrapportering/
    │
    ├── README.md
    ├── .gitignore
    ├── requirements.txt
    │
    ├── archive/
    │   └── upload_file_mp.py  # possible other option for uploading files with multiprocessing (still some issues)
    │
    ├── automation/
    │   ├── run_script.bat    # batch file for running the main script automaticaly with task scheduler
    │
    ├── data/
    │   ├── Log.txt    # keeps track of the uploaded files with timestamps
    │   ├── source_paths.json    # Contains the needed by the python script
    │   ├── credentials.json    # contains the credentials for the google drive service account
    │   ├── token.json    # contains the token of the service account
    │   └── dates.json    # contains the name of the files uploaded the previous time 
    │
    ├── project/
    │   ├── src/    # contains the .py files needed to run the project
    │   │   ├── Merge.py    # contains all functions to load and save the json files and merge csv files together
    │   │   ├── OpenAlarmsExcelFile.py    # contains all funcions needed to make the open alarm excel file of the open alarms log
    │   │   ├── StatisticalReport.py    # contains all functions needed to make a report.csv of the log.csv
    │   │   ├── TerugkoppelingExcelFile.py    # contains all funcions needed to make the report excel file of the log.csv and the report.csv
    │   │   ├── UploadFile.py    #contains all functions needed for uploading files to a shared google drive
    │   │   └── main.py    # serves as the entry point for the program, coordinating the execution of other modules and scripts.
    │   │
    │   └── test/    # analog to src/ folder but for testing
    │       ├── Merge_test.py
    │       ├── OpenAlarmsExcelFile_test.py
    │       ├── StatisticalReport_test.py
    │       ├── TerugkoppelingExcelFile_test.py
    │       ├── UploadFile_test.py
    │       ├── main_single.py
    │       ├── main_test.py

## Gebruik

Nadat de installatie voltooid is zijn er nog aantal stappen nodig voordat het script volledig operationeel is. Eerst moeten de paden gespecifeerd worden in het bestand "source_paths.json"

- iris_log: het pad waar de dagelijkse log wordt weggeschreven.
- open_alarms_log: het pad waar de dagelijkse log met openstaande alarmen wordt weggeschreven.
- week_month_log_folder: het pad waar de wekelijkse en maandelijkse log worden weggeschreven.

Noteer wel dat de urls met een dubbele backslash ingegeven moeten worden anders geeft de json file een foutmelding. Daarnaast kunnen de paden voor het testen ook worden ingegeven. 
Deze volgen de analoog hierboven beschreven tekst.

Om bestanden te kunnen uploaden op een google drive is een service account nodig en de bijhorende credentials file. Deze kunnen aangemaakt worden via:
```bash
    https://console.cloud.google.com/
```
Verdere uitleg is te vinden op:
```bash
    https://developers.google.com/workspace/guides/create-credentials
```

Via de batch bestanden en de task scheduler kan de script automatisch lopen. Vergeet wel niet het juiste pad naar het batch bestand in te geven voor de actie. In het batch bestand zelf moet dan ook de venv_root_dir% aangevuld worden met de pad waar de project-map IRIS-alarmrapportering is weggeschreven na de klonen van de git repository. 

## Code 
Hieronder is de nodige code te vinden om het script volledig te laten werken. De mappen moeten aangemaakt worden volgens de opbouw voorgeschreven in de [Mappenstructuur](#Mappenstructuur).

**1. source_paths.json**:
Dit bestand moet aangemaakt worden in de data folder. 
```bash
    {
    "iris_log": ,
    "open_alarms_log": ,
    "week_month_log_folder": ,
    "iris_log_test": ,
    "open_alarms_log_test": ,
    "week_month_log_folder_test":  
    }
```
**2. run_script.bat**:
Dit bestand moet aangemaakt worden in de automation folder.
```bash
    REM    Windows batch script to run 1+ Python program/scripts, sequentially, within their virtual environment. This can be called from Windows Task Scheduler.


    set original_dir=%CD%
    set venv_root_dir= # insert path to the project directory

    cd %venv_root_dir%

    call %venv_root_dir%\.venv\Scripts\activate.bat

    py .\project\src\main.py # for the test script edit main.py to main_test.py

    call %venv_root_dir%\.venv\Scripts\deactivate.bat

    cd %original_dir%

    exit /B 1
```

##  Licentie (MIT)
Dit project is gelicentieerd onder de MIT-licentie - zie het bestand LICENSE.txt voor details.
