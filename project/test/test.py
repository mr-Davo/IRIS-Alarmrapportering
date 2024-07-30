from datetime import datetime
from dateutil.relativedelta import relativedelta

# Get the input date from the user in 'y-m' format
input_date_str = input("Enter a date in the format 'y-m' (e.g., 2024-07): ")

# Convert the input string to a datetime object
input_date = datetime.strptime(input_date_str, "%Y-%m")

# Calculate the date 6 months prior
six_months_prior_date = input_date - relativedelta(months=6)

# Extract the year and month from the calculated date
six_months_prior_year_month = six_months_prior_date.strftime("%Y-%m")

# Print the result
print(f"The date 6 months prior to now is: {six_months_prior_year_month}")
