import pandas as pd
import json
import os

# Load the IPUMS variable definitions
with open('ipums_variables.json', 'r') as f:
    ipums_vars = json.load(f)

# Directory containing dimension tables
star_dir = 'star_schema'

def verify_dim_table(table_name, var_name):
    """Verify a dimension table against IPUMS definitions"""
    file_path = os.path.join(star_dir, f'dim_{table_name.lower()}.csv')
    if not os.path.exists(file_path):
        print(f"❌ {file_path} does not exist")
        return
    
    # Read dimension table
    dim_df = pd.read_csv(file_path)
    print(f"\nVerifying {file_path}...")
    print(f"Table has {len(dim_df):,} records")
    
    # Get IPUMS codes
    ipums_codes = ipums_vars[var_name]['codes']
    
    # Check if all codes in the dimension table have valid descriptions
    value_col = f'{var_name}_value'
    code_col = var_name
    
    if code_col not in dim_df.columns:
        print(f"❌ Column {code_col} not found in table")
        return
    if value_col not in dim_df.columns:
        print(f"❌ Column {value_col} not found in table")
        return
    
    # Convert codes to strings for comparison
    dim_df[code_col] = dim_df[code_col].astype(str)
    
    # Check for missing codes
    dim_codes = set(dim_df[code_col].unique())
    ipums_code_set = set(ipums_codes.keys())
    
    missing_codes = ipums_code_set - dim_codes
    extra_codes = dim_codes - ipums_code_set
    
    if missing_codes:
        print(f"❌ Missing codes in dimension table: {sorted(missing_codes)}")
    else:
        print("✓ All IPUMS codes are present in dimension table")
    
    if extra_codes:
        print(f"⚠️ Extra codes in dimension table: {sorted(extra_codes)}")
    
    # Check descriptions
    for idx, row in dim_df.iterrows():
        code = row[code_col]
        value = row[value_col]
        if code in ipums_codes:
            expected_value = ipums_codes[code]
            if value != expected_value:
                print(f"❌ Mismatch for code {code}:")
                print(f"   Expected: {expected_value}")
                print(f"   Found:    {value}")

# Verify key dimension tables
tables_to_verify = [
    ('statefip', 'STATEFIP'),
    ('educd', 'EDUCD'),
    ('raced', 'RACED'),
    ('languaged', 'LANGUAGED'),
    ('empstatd', 'EMPSTATD')
]

for table_name, var_name in tables_to_verify:
    verify_dim_table(table_name, var_name) 