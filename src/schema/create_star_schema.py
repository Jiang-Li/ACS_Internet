"""
Create a star schema from ACS data.
This script transforms raw ACS data into a dimensional model for analysis.
"""

import pandas as pd
import numpy as np
import os
import json
from pathlib import Path

# Get the project root directory (2 levels up from this script)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

class StarSchemaBuilder:
    def __init__(self, input_file=None, output_dir=None, ipums_json=None):
        """Initialize the star schema builder.
        
        Args:
            input_file (str): Path to input CSV file
            output_dir (str): Directory to save star schema files
            ipums_json (str): Path to IPUMS variable definitions JSON
        """
        # Set default paths relative to project root if not provided
        if input_file is None:
            input_file = PROJECT_ROOT / 'data/raw/usa_2023_subset.csv'
        if output_dir is None:
            output_dir = PROJECT_ROOT / 'data/processed/star_schema'
        if ipums_json is None:
            ipums_json = PROJECT_ROOT / 'data/raw/ipums_variables.json'
            
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.ipums_json = Path(ipums_json)
        self.fact_df = None
        self.ipums_vars = None
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_data(self):
        """Load the input data and IPUMS definitions."""
        print(f"Reading dataset from: {self.input_file}")
        self.fact_df = pd.read_csv(self.input_file)
        print(f"Fact table has {len(self.fact_df):,} records")
        
        print(f"Reading IPUMS definitions from: {self.ipums_json}")
        with open(self.ipums_json, 'r') as f:
            self.ipums_vars = json.load(f)
    
    def create_dimension_tables(self):
        """Create dimension tables from IPUMS definitions."""
        for var_name, var_info in self.ipums_vars.items():
            print(f"Creating dimension table for {var_name}...")
            
            # Create dimension table from IPUMS codes
            dim_data = []
            for code, description in var_info['codes'].items():
                dim_data.append({
                    var_name: int(code),
                    f'{var_name}_value': description
                })
            
            dim_df = pd.DataFrame(dim_data)
            dim_file = self.output_dir / f'dim_{var_name.lower()}.csv'
            dim_df.to_csv(dim_file, index=False)
            print(f"  - Saved {dim_file} with {len(dim_df)} records")
    
    def create_age_groups(self):
        """Create age groups dimension table."""
        if 'AGE' not in self.fact_df.columns:
            return
            
        age_groups = [
            (0, 4, 'Under 5'),
            (5, 17, '5-17'),
            (18, 24, '18-24'),
            (25, 34, '25-34'),
            (35, 44, '35-44'),
            (45, 54, '45-54'),
            (55, 64, '55-64'),
            (65, 74, '65-74'),
            (75, 120, '75+')
        ]
        
        age_data = []
        for min_age, max_age, label in age_groups:
            for age in range(min_age, max_age + 1):
                age_data.append({
                    'AGE': age,
                    'AGE_group': label
                })
        
        age_df = pd.DataFrame(age_data)
        age_file = self.output_dir / 'dim_age.csv'
        age_df.to_csv(age_file, index=False)
        print(f"  - Saved {age_file} with {len(age_df)} records")
    
    def create_income_groups(self):
        """Create income groups dimension table."""
        if 'INCTOT' not in self.fact_df.columns:
            return
            
        incomes = self.fact_df['INCTOT'].unique()
        income_groups = [
            (-10000000, 0, 'Negative or Zero'),
            (1, 9999, 'Under $10,000'),
            (10000, 24999, '$10,000-$24,999'),
            (25000, 49999, '$25,000-$49,999'),
            (50000, 74999, '$50,000-$74,999'),
            (75000, 99999, '$75,000-$99,999'),
            (100000, 149999, '$100,000-$149,999'),
            (150000, 10000000, '$150,000+')
        ]
        
        income_data = []
        for income in sorted(incomes):
            group = 'Unknown'
            for min_val, max_val, label in income_groups:
                if min_val <= income <= max_val:
                    group = label
                    break
            
            income_data.append({
                'INCTOT': income,
                'INCTOT_group': group
            })
        
        income_df = pd.DataFrame(income_data)
        income_file = self.output_dir / 'dim_income.csv'
        income_df.to_csv(income_file, index=False)
        print(f"  - Saved {income_file} with {len(income_df)} records")
    
    def create_household_income_groups(self):
        """Create household income groups dimension table."""
        if 'HHINCOME' not in self.fact_df.columns:
            return
            
        hh_incomes = self.fact_df['HHINCOME'].unique()
        hhincome_groups = [
            (-10000000, 0, 'Negative or Zero'),
            (1, 24999, 'Under $25,000'),
            (25000, 49999, '$25,000-$49,999'),
            (50000, 74999, '$50,000-$74,999'),
            (75000, 99999, '$75,000-$99,999'),
            (100000, 149999, '$100,000-$149,999'),
            (150000, 199999, '$150,000-$199,999'),
            (200000, 10000000, '$200,000+'),
            (9999999, 9999999, 'N/A or Missing')
        ]
        
        hhincome_data = []
        for income in sorted(hh_incomes):
            group = 'Unknown'
            for min_val, max_val, label in hhincome_groups:
                if min_val <= income <= max_val:
                    group = label
                    break
            
            hhincome_data.append({
                'HHINCOME': income,
                'HHINCOME_group': group
            })
        
        hhincome_df = pd.DataFrame(hhincome_data)
        hhincome_file = self.output_dir / 'dim_hhincome.csv'
        hhincome_df.to_csv(hhincome_file, index=False)
        print(f"  - Saved {hhincome_file} with {len(hhincome_df)} records")
    
    def save_fact_table(self):
        """Save the fact table."""
        fact_file = self.output_dir / 'fact_acs_2023.csv'
        self.fact_df.to_csv(fact_file, index=False)
        print(f"\nSaved fact table: {fact_file} with {len(self.fact_df):,} records")
    
    def print_schema_structure(self):
        """Print the star schema structure."""
        print("\nStar Schema Structure:")
        print("=====================")
        print("Fact Table:")
        print(f"  - fact_acs_2023.csv ({len(self.fact_df):,} records)")
        print("  - Contains measures: PERWT (person weight for population estimates)")
        print("\nDimension Tables:")
        for file in sorted(os.listdir(self.output_dir)):
            if file.startswith('dim_'):
                file_path = self.output_dir / file
                dim_count = len(pd.read_csv(file_path))
                print(f"  - {file} ({dim_count:,} records)")
    
    def create_schema(self):
        """Create the complete star schema."""
        try:
            self.load_data()
            self.create_dimension_tables()
            self.create_age_groups()
            self.create_income_groups()
            self.create_household_income_groups()
            self.save_fact_table()
            self.print_schema_structure()
            print("\nStar schema created successfully!")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

def main():
    """Main function to create the star schema."""
    builder = StarSchemaBuilder()
    builder.create_schema()

if __name__ == '__main__':
    main() 