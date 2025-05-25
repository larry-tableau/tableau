# Import necessary libraries for loan application data generation
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from google.colab import files

def generate_loan_application_dataset(num_rows=150000, outlier_fraction=0.02):
    """
    Generate realistic loan application data for Bendigo and Adelaide Bank
    
    Parameters:
    - num_rows: Number of loan application records to generate (default: 150,000)
    - outlier_fraction: Percentage of records with outlier values (default: 2%)
    
    Returns:
    - pandas DataFrame with loan application data
    """
    
    # Set seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    print(f"Generating {num_rows:,} loan application records...")
    
    # Define date ranges (last 3 years as specified)
    end_date = datetime(2025, 5, 24, 23, 59, 59)
    start_date = datetime(2022, 5, 1, 0, 0, 0)
    
    # Generate unique Application IDs (sequential)
    application_ids = [f"APP-{str(i).zfill(7)}" for i in range(1, num_rows + 1)]
    
    # Generate Customer IDs (allowing multiple applications per customer)
    unique_customer_count = 35000  # Pool of 35,000 unique customers
    customer_ids = [f"CUST-{str(i).zfill(5)}" for i in range(1, unique_customer_count + 1)]
    
    # Australian states with realistic distribution (VIC, NSW, QLD, SA focus)
    states = ['VIC', 'NSW', 'QLD', 'SA', 'WA', 'TAS', 'NT', 'ACT']
    state_weights = [0.28, 0.32, 0.18, 0.12, 0.06, 0.02, 0.01, 0.01]
    
    # Australian postcodes by state (representative samples)
    postcodes_by_state = {
        'VIC': ['3000', '3001', '3002', '3006', '3008', '3121', '3141', '3181', '3182', '3183', 
                '3124', '3125', '3126', '3127', '3128', '3129', '3130', '3131', '3132', '3133',
                '3134', '3135', '3136', '3137', '3138', '3139', '3140', '3142', '3143', '3144'],
        'NSW': ['2000', '2001', '2002', '2006', '2007', '2008', '2009', '2010', '2011', '2015',
                '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025',
                '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035'],
        'QLD': ['4000', '4001', '4002', '4003', '4004', '4005', '4006', '4007', '4008', '4009',
                '4010', '4011', '4012', '4013', '4014', '4015', '4016', '4017', '4018', '4019',
                '4020', '4021', '4022', '4023', '4024', '4025', '4026', '4027', '4028', '4029'],
        'SA': ['5000', '5001', '5002', '5003', '5004', '5005', '5006', '5007', '5008', '5009',
               '5010', '5011', '5012', '5013', '5014', '5015', '5016', '5017', '5018', '5019'],
        'WA': ['6000', '6001', '6002', '6003', '6004', '6005', '6006', '6007', '6008', '6009'],
        'TAS': ['7000', '7001', '7002', '7003', '7004', '7005', '7006', '7007', '7008', '7009'],
        'NT': ['0800', '0801', '0802', '0803', '0804', '0805', '0806', '0807', '0808', '0809'],
        'ACT': ['2600', '2601', '2602', '2603', '2604', '2605', '2606', '2607', '2608', '2609']
    }
    
    # Region mapping for postcodes
    region_mapping = {
        'VIC': 'Metro Melbourne', 'NSW': 'Metro Sydney', 'QLD': 'Metro Brisbane',
        'SA': 'Metro Adelaide', 'WA': 'Metro Perth', 'TAS': 'Regional Tasmania',
        'NT': 'Regional Northern Territory', 'ACT': 'Metro Canberra'
    }
    
    # Loan types with realistic weights for Australian market
    loan_types = ['Fixed Rate Home Loan', 'Variable Rate Home Loan', 'Investment Property Loan', 
                  'First Home Buyer Special', 'Refinance Special']
    loan_type_weights = [0.35, 0.30, 0.15, 0.12, 0.08]
    
    # Loan purposes
    loan_purposes = ['New Property Purchase', 'Refinance Existing Loan', 'Home Equity Release', 
                     'Investment Property Purchase']
    loan_purpose_weights = [0.45, 0.30, 0.10, 0.15]
    
    # Application channels with digital preference
    application_channels = ['Online Portal', 'Mobile App', 'Broker Network A', 'Broker Network B', 
                           'Branch - City Center', 'Branch - Suburban East', 'Phone Application']
    channel_weights = [0.35, 0.25, 0.15, 0.10, 0.08, 0.05, 0.02]
    
    # Lead sources
    lead_sources = ['Google Ads', 'Facebook Campaign', 'RealEstate.com.au', 'Broker Network A',
                   'Branch Walk-in', 'Customer Referral', 'Existing Customer Email', 'Organic Search']
    lead_source_weights = [0.20, 0.15, 0.18, 0.15, 0.08, 0.12, 0.07, 0.05]
    
    # Decision outcomes with realistic approval rates
    decision_outcomes = ['Approved', 'Declined', 'Withdrawn by Applicant', 'Conditionally Approved']
    outcome_weights = [0.60, 0.25, 0.10, 0.05]
    
    # Customer segments
    customer_segments = ['First Home Buyer', 'Property Investor', 'Refinancer', 
                        'Upgrader/Downsizer', 'Self-Employed Professional']
    segment_weights = [0.30, 0.20, 0.25, 0.15, 0.10]
    
    # Competitor banks for refinancing
    competitor_banks = ['Commonwealth Bank', 'Westpac', 'NAB', 'ANZ', 'Macquarie Bank',
                       'ING Direct', 'Other Financial Institution']
    
    # Generate loan officer and branch IDs
    loan_officer_ids = [f"LO-{str(i).zfill(3)}" for i in range(1, 151)]  # 150 loan officers
    branch_ids = [f"BR-MELB-{str(i).zfill(2)}" for i in range(1, 16)] + \
                 [f"BR-ADEL-{str(i).zfill(2)}" for i in range(1, 11)] + \
                 [f"BR-BRIS-{str(i).zfill(2)}" for i in range(1, 8)] + \
                 [f"BR-PERTH-{str(i).zfill(2)}" for i in range(1, 6)]
    
    # Initialize data dictionary
    data = {}
    
    # Generate basic identifiers
    data['Application_ID'] = application_ids
    data['Customer_ID'] = np.random.choice(customer_ids, size=num_rows, replace=True)
    
    # Generate timestamps with business hours bias (9 AM - 5 PM weekdays)
    def generate_business_hour_timestamp():
        # Random date in range
        days_diff = (end_date - start_date).days
        random_days = np.random.randint(0, days_diff, num_rows)
        base_dates = [start_date + timedelta(days=int(d)) for d in random_days]
        
        timestamps = []
        for base_date in base_dates:
            # 70% chance of business hours (9-17), 30% chance of any hour
            if np.random.random() < 0.7 and base_date.weekday() < 5:  # Weekday
                hour = np.random.randint(9, 17)
            else:
                hour = np.random.randint(0, 24)
            
            minute = np.random.randint(0, 60)
            second = np.random.randint(0, 60)
            
            timestamp = base_date.replace(hour=hour, minute=minute, second=second)
            timestamps.append(timestamp)
        
        return timestamps
    
    event_timestamps = generate_business_hour_timestamp()
    data['Event_Timestamp_UTC'] = event_timestamps
    data['Event_Date'] = [ts.date() for ts in event_timestamps]
    data['Application_Submitted_Hour_Of_Day'] = [ts.hour for ts in event_timestamps]
    
    # Generate geographic data
    selected_states = np.random.choice(states, size=num_rows, p=state_weights)
    data['Property_State'] = selected_states
    
    # Generate postcodes based on states
    postcodes = []
    regions = []
    for state in selected_states:
        postcode = np.random.choice(postcodes_by_state[state])
        postcodes.append(postcode)
        regions.append(region_mapping[state])
    
    data['Property_Postcode'] = postcodes
    data['Property_Region_Name'] = regions
    
    # Generate categorical data
    data['Loan_Type'] = np.random.choice(loan_types, size=num_rows, p=loan_type_weights)
    data['Loan_Purpose'] = np.random.choice(loan_purposes, size=num_rows, p=loan_purpose_weights)
    data['Application_Channel'] = np.random.choice(application_channels, size=num_rows, p=channel_weights)
    data['Lead_Source'] = np.random.choice(lead_sources, size=num_rows, p=lead_source_weights)
    data['Decision_Outcome'] = np.random.choice(decision_outcomes, size=num_rows, p=outcome_weights)
    data['Customer_Segment'] = np.random.choice(customer_segments, size=num_rows, p=segment_weights)
    
    # Generate loan officer IDs
    data['Loan_Officer_ID'] = np.random.choice(loan_officer_ids, size=num_rows)
    
    # Generate branch IDs (only for branch channels)
    branch_id_list = []
    for channel in data['Application_Channel']:
        if 'Branch' in channel:
            branch_id_list.append(np.random.choice(branch_ids))
        else:
            branch_id_list.append(None)
    data['Branch_ID'] = branch_id_list
    
    # Generate competitor bank data (only for refinancing)
    competitor_list = []
    for purpose in data['Loan_Purpose']:
        if purpose == 'Refinance Existing Loan':
            competitor_list.append(np.random.choice(competitor_banks))
        else:
            competitor_list.append(None)
    data['Competitor_Bank_Refinanced_From'] = competitor_list
    
    # Generate financial data
    # Loan amounts with realistic distribution
    loan_amounts = np.random.normal(450000, 150000, num_rows)
    loan_amounts = np.clip(loan_amounts, 50000, 2000000)
    data['Loan_Amount_Requested_AUD'] = np.round(loan_amounts, 2)
    
    # Property valuations (typically higher than loan amount)
    lvr_ratios = np.random.uniform(0.6, 0.95, num_rows)
    property_valuations = data['Loan_Amount_Requested_AUD'] / lvr_ratios
    property_valuations = np.clip(property_valuations, 100000, 3000000)
    data['Property_Valuation_AUD'] = np.round(property_valuations, 2)
    
    # Credit scores with realistic distribution
    credit_scores = np.random.normal(700, 80, num_rows)
    credit_scores = np.clip(credit_scores, 300, 850).astype(int)
    data['Customer_Credit_Score'] = credit_scores
    
    # Generate decision and settlement dates
    decision_dates = []
    settlement_dates = []
    processing_times = []
    settlement_durations = []
    
    for i, (event_date, outcome) in enumerate(zip(data['Event_Date'], data['Decision_Outcome'])):
        # Decision date (1-30 days after application, log-normal distribution)
        if outcome != 'Withdrawn by Applicant' or np.random.random() < 0.9:  # 90% have decisions
            days_to_decision = max(1, int(np.random.lognormal(2.0, 0.8)))
            days_to_decision = min(days_to_decision, 30)
            decision_date = event_date + timedelta(days=days_to_decision)
            decision_dates.append(decision_date)
            processing_times.append(days_to_decision)
            
            # Settlement date (only for approved loans)
            if outcome in ['Approved', 'Conditionally Approved'] and np.random.random() < 0.85:  # 85% settle
                days_to_settlement = np.random.randint(7, 61)  # 7-60 days after decision
                settlement_date = decision_date + timedelta(days=days_to_settlement)
                settlement_dates.append(settlement_date)
                settlement_durations.append((settlement_date - event_date).days)
            else:
                settlement_dates.append(None)
                settlement_durations.append(None)
        else:
            decision_dates.append(None)
            settlement_dates.append(None)
            processing_times.append(None)
            settlement_durations.append(None)
    
    data['Decision_Date'] = decision_dates
    data['Settlement_Date'] = settlement_dates
    data['Application_Processing_Time_To_Decision_Days'] = processing_times
    data['Loan_Settlement_Duration_Days'] = settlement_durations
    
    # Generate application status based on dates and outcomes
    current_statuses = []
    for outcome, decision_date, settlement_date in zip(data['Decision_Outcome'], 
                                                      data['Decision_Date'], 
                                                      data['Settlement_Date']):
        if settlement_date is not None:
            current_statuses.append('Settled')
        elif outcome == 'Approved' and decision_date is not None:
            current_statuses.append('Offer Issued')
        elif outcome == 'Declined':
            current_statuses.append('Closed - Declined')
        elif outcome == 'Withdrawn by Applicant':
            current_statuses.append('Closed - Withdrawn')
        elif decision_date is not None:
            current_statuses.append('Pending Final Review')
        else:
            current_statuses.append('Under Assessment')
    
    data['Application_Current_Status'] = current_statuses
    
    # Generate approved loan amounts and interest rates
    approved_amounts = []
    interest_rates = []
    
    for i, outcome in enumerate(data['Decision_Outcome']):
        if outcome in ['Approved', 'Conditionally Approved']:
            # Approved amount (90-100% of requested)
            approval_ratio = np.random.uniform(0.90, 1.00)
            approved_amount = data['Loan_Amount_Requested_AUD'][i] * approval_ratio
            approved_amounts.append(round(approved_amount, 2))
            
            # Interest rate based on credit score and loan type
            base_rate = 5.5
            credit_adjustment = (750 - data['Customer_Credit_Score'][i]) * 0.01
            rate_variation = np.random.normal(0, 0.3)
            interest_rate = base_rate + credit_adjustment + rate_variation
            interest_rate = max(3.0, min(7.5, interest_rate))
            interest_rates.append(round(interest_rate, 2))
        else:
            approved_amounts.append(0.0)
            interest_rates.append(None)
    
    data['Loan_Amount_Approved_AUD'] = approved_amounts
    data['Interest_Rate_Offered_Percent'] = interest_rates
    
    # Calculate LVR for approved loans
    lvr_percentages = []
    for approved_amt, property_val in zip(data['Loan_Amount_Approved_AUD'], 
                                         data['Property_Valuation_AUD']):
        if approved_amt > 0:
            lvr = (approved_amt / property_val) * 100
            lvr_percentages.append(round(lvr, 2))
        else:
            lvr_percentages.append(None)
    
    data['Loan_To_Value_Ratio_LVR_Percent'] = lvr_percentages
    
    # Generate flag columns
    data['Is_Online_Application_Flag'] = [
        1 if channel in ['Online Portal', 'Mobile App'] else 0 
        for channel in data['Application_Channel']
    ]
    
    data['Is_Approved_Application_Flag'] = [
        1 if outcome in ['Approved', 'Conditionally Approved'] else 0 
        for outcome in data['Decision_Outcome']
    ]
    
    data['Is_Settled_Application_Flag'] = [
        1 if settlement_date is not None else 0 
        for settlement_date in data['Settlement_Date']
    ]
    
    # Application record count (always 1)
    data['Application_Record_Count'] = [1] * num_rows
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add realistic outliers for recent applications (last 30 days)
    recent_cutoff = end_date - timedelta(days=30)
    recent_mask = df['Event_Timestamp_UTC'] >= recent_cutoff
    recent_indices = df[recent_mask].index
    
    if len(recent_indices) > 0:
        # Select outlier indices
        outlier_count = int(len(recent_indices) * outlier_fraction)
        outlier_indices = np.random.choice(recent_indices, size=outlier_count, replace=False)
        
        # Apply outliers to loan amounts and property valuations
        for idx in outlier_indices:
            if np.random.random() < 0.5:  # High-value outlier
                df.at[idx, 'Loan_Amount_Requested_AUD'] *= np.random.uniform(2.0, 4.0)
                df.at[idx, 'Property_Valuation_AUD'] *= np.random.uniform(2.0, 4.0)
            else:  # Processing time outlier
                if df.at[idx, 'Application_Processing_Time_To_Decision_Days'] is not None:
                    df.at[idx, 'Application_Processing_Time_To_Decision_Days'] *= np.random.randint(2, 5)
    
    # Format dates for output
    df['Event_Date'] = pd.to_datetime(df['Event_Date']).dt.strftime('%d/%m/%Y')
    df['Decision_Date'] = pd.to_datetime(df['Decision_Date']).dt.strftime('%d/%m/%Y')
    df['Settlement_Date'] = pd.to_datetime(df['Settlement_Date']).dt.strftime('%d/%m/%Y')
    df['Event_Timestamp_UTC'] = pd.to_datetime(df['Event_Timestamp_UTC']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"Dataset generation complete! Generated {len(df):,} loan application records.")
    print(f"Approval rate: {df['Is_Approved_Application_Flag'].mean():.1%}")
    print(f"Settlement rate: {df['Is_Settled_Application_Flag'].mean():.1%}")
    print(f"Online application rate: {df['Is_Online_Application_Flag'].mean():.1%}")
    
    return df

# Generate the loan application dataset
loan_dataset = generate_loan_application_dataset(num_rows=150000, outlier_fraction=0.02)

# Display sample of the dataset
print("\nSample of generated data:")
print(loan_dataset.head(10))

print(f"\nDataset shape: {loan_dataset.shape}")
print(f"Columns: {list(loan_dataset.columns)}")

# Save to CSV file
csv_filename = 'bendigo_adelaide_bank_loan_applications.csv'
hyper_filename = 'bendigo_adelaide_bank_loan_applications.hyper'
loan_dataset.to_csv(csv_filename, index=False)
pantab.frame_to_hyper(loan_dataset, hyper_filename, table='HomeLoans')
print(f"\nDataset saved as '{csv_filename}' and '{hyper_filename}")

# Download the file
# files.download(csv_filename)

# Display summary statistics
print("\nSummary Statistics:")
print(f"Total Applications: {len(loan_dataset):,}")
print(f"Unique Customers: {loan_dataset['Customer_ID'].nunique():,}")
print(f"Date Range: {loan_dataset['Event_Date'].min()} to {loan_dataset['Event_Date'].max()}")
print(f"Average Loan Amount Requested: ${loan_dataset['Loan_Amount_Requested_AUD'].mean():,.2f}")
print(f"Average Property Valuation: ${loan_dataset['Property_Valuation_AUD'].mean():,.2f}")
print(f"Average Credit Score: {loan_dataset['Customer_Credit_Score'].mean():.0f}")

# Show distribution by key dimensions
print(f"\nTop 5 States by Application Volume:")
print(loan_dataset['Property_State'].value_counts().head())

print(f"\nTop 5 Loan Types:")
print(loan_dataset['Loan_Type'].value_counts().head())

print(f"\nApplication Channel Distribution:")
print(loan_dataset['Application_Channel'].value_counts())
