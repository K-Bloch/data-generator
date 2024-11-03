import pandas as pd
import random
from datetime import datetime
from faker import Faker

# Initialize Faker with Polish locale
fake = Faker('pl_PL')

# User-configurable variables
num_donors = 5099  # Total number of donors
earliest_year = 2020  # Earliest year for donation dates
latest_year = 2024  # Latest year for donation dates

# Function to generate unique donation dates
def generate_unique_dates(start_year, end_year, total_dates):
    unique_dates = set()
    while len(unique_dates) < total_dates:
        # Generate a random year and month
        random_year = random.randint(start_year, end_year)
        random_month = random.randint(1, 12)
        # Ensure the day is valid for the generated month and year
        day = random.randint(1, 28)  # Using 28 to avoid month-end issues
        unique_dates.add(datetime(random_year, random_month, day))

    return sorted(unique_dates)

# Function to generate donor data
def generate_donor_data(num_donors, earliest_year, latest_year):
    donor_data = []
    acquisition_channels = ['Online Event', 'In-Person Event', 'Social Media', 'Direct Mail', 'Partnership']

    # Define donor types and their corresponding weights
    donor_types = ['Individual', 'Organization']
    donor_type_weights = [70, 30]  # Corresponding weights for Individual and Organization

    # Define gender options and their corresponding weights
    genders = ['Male', 'Female', 'Non-binary']
    gender_weights = [49, 49, 2]  # Corresponding weights for each gender

    for donor_id in range(1, num_donors + 1):
        # Determine donor type based on weighted probabilities
        donor_type = random.choices(donor_types, weights=donor_type_weights)[0]

        # Generate a number of donation dates (number of donations) - between 1 and 10
        total_donations = random.randint(1, 10)
        donation_dates = generate_unique_dates(earliest_year, latest_year, total_donations)

        # Generate donation amounts based on donor type
        if donor_type == 'Individual':
            base_amount = random.randint(6, 400)  # Base amount for individuals
            donation_amounts = [base_amount + random.randint(-5, 15) for _ in range(total_donations)]
        else:  # Organization
            base_amount = random.randint(1000, 10000)  # Base amount for organizations
            donation_amounts = [base_amount + random.randint(-500, 1000) for _ in range(total_donations)]

        # Append donor data with required columns
        donor_data.append({
            'Donor ID': donor_id,
            'Donor Type': donor_type,
            'Donation Dates': ', '.join(date.strftime('%Y-%m-%d') for date in donation_dates),
            'Donation Amounts': ', '.join(map(str, donation_amounts)),
            'Acquisition Channel': random.choice(acquisition_channels),
            'Age': random.randint(18, 90),
            'Gender': random.choices(genders, weights=gender_weights)[0],  # Weighted selection of gender
            'Location': f"{fake.city()}, Poland"  # Random city from Faker with Polish locale
        })
    
    return pd.DataFrame(donor_data)

# Generate the dataset
donor_dataset = generate_donor_data(num_donors, earliest_year, latest_year)

# Save the dataset to a CSV file
donor_dataset.to_csv('D:/Documents/donor_data.csv', index=False)

print(donor_dataset.head())  # Display first few records