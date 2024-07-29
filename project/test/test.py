
import pandas as pd
from StatisticalReport_test import ReformatDate

log = r"C:\Users\daana\docs\werk\AWV\IRIS-alarmrapportering\Logboek IRIS\test3.csv"
total_df = pd.read_csv(log, sep =",")

print(total_df)

et = ReformatDate(total_df.iloc[:,5])  
print(et)

Eindt = pd.to_datetime(et, errors='coerce',format= "%H:%M:%S %d/%m/%Y", dayfirst=True)

Eindt = pd.to_datetime(et)

print(Eindt)