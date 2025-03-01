"""
Create a star schema from ACS data.
This script transforms raw ACS data into a dimensional model for analysis.
Supports reading from compressed CSV files (.gz, .zip, .bz2, .xz, .zst).
"""

import pandas as pd
import numpy as np
import os
import xml.etree.ElementTree as ET
from pathlib import Path

# Get the project root directory (1 level up from this script)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define measure variables
MEASURE_VARS = ['PERWT', 'AGE', 'HHINCOME', 'INCTOT']
EXCLUDE_VARS = ['PERNUM', 'YEAR']

# Define XML namespace
NS = {'ddi': 'ddi:codebook:2_5'}

class StarSchemaBuilder:
    def __init__(self, input_file=None, output_dir=None, ipums_xml=None):
        """Initialize the star schema builder.
        
        Args:
            input_file (str): Path to input CSV file (can be compressed: .gz, .zip, .bz2, .xz, .zst)
            output_dir (str): Directory to save star schema files
            ipums_xml (str): Path to IPUMS variable definitions XML
        """
        # Set default paths relative to project root if not provided
        if input_file is None:
            input_file = PROJECT_ROOT / 'data/raw/usa_2023_subset.csv.zip'
        if output_dir is None:
            output_dir = PROJECT_ROOT / 'data/processed/star_schema'
        if ipums_xml is None:
            ipums_xml = PROJECT_ROOT / 'data/raw/ipums_variables.xml'
            
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.ipums_xml = Path(ipums_xml)
        self.fact_df = None
        self.ipums_vars = None
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_data(self):
        """Load the input data and IPUMS definitions."""
        print(f"Reading dataset from: {self.input_file}")
        
        try:
            # Get the filename inside the ZIP
            import zipfile
            with zipfile.ZipFile(self.input_file, 'r') as zip_ref:
                self.input_csv_name = zip_ref.namelist()[0]
            
            # Read the CSV using the exact same format
            self.fact_df = pd.read_csv(
                self.input_file,
                compression={'method': 'zip', 'archive_name': self.input_csv_name}
            )
            print(f"Fact table has {len(self.fact_df):,} records")
            
            # Print variables that need dimension tables
            dim_vars = [col for col in self.fact_df.columns 
                       if col not in MEASURE_VARS and col not in EXCLUDE_VARS]
            print(f"\nVariables requiring dimension tables: {', '.join(sorted(dim_vars))}")
            
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
            raise
        
        print(f"\nReading IPUMS definitions from: {self.ipums_xml}")
        try:
            # Parse XML file
            tree = ET.parse(self.ipums_xml)
            root = tree.getroot()
            
            # Convert XML to dictionary format
            self.ipums_vars = {}
            
            # Find all variables in the DDI format
            for var in root.findall('.//ddi:var', NS):
                var_name = var.get('name')
                if not var_name:
                    continue
                
                # Get variable description
                desc_elem = var.find('.//ddi:labl', NS)
                desc = desc_elem.text if desc_elem is not None else ''
                
                self.ipums_vars[var_name] = {
                    'desc': desc,
                    'codes': {}
                }
                
                # Get codes and descriptions from DDI format
                for catgry in var.findall('.//ddi:catgry', NS):
                    code_elem = catgry.find('ddi:catValu', NS)
                    label_elem = catgry.find('ddi:labl', NS)
                    
                    if code_elem is not None and label_elem is not None:
                        code_value = code_elem.text
                        code_label = label_elem.text
                        if code_value and code_label:
                            self.ipums_vars[var_name]['codes'][code_value] = code_label
            
            # Print variables found in XML
            xml_vars = sorted(self.ipums_vars.keys())
            print(f"\nVariables found in XML: {', '.join(xml_vars)}")
            
            # Check which variables are missing definitions
            dim_vars = [col for col in self.fact_df.columns 
                       if col not in MEASURE_VARS and col not in EXCLUDE_VARS]
            missing_defs = [var for var in dim_vars if var not in self.ipums_vars]
            if missing_defs:
                print(f"\nWARNING: The following variables are missing definitions:")
                for var in sorted(missing_defs):
                    print(f"  - {var}")
                    
        except Exception as e:
            print(f"Error reading XML file: {str(e)}")
            raise

    def create_dimension_tables(self):
        """Create dimension tables from IPUMS definitions."""
        # Get all non-measure variables that need dimension tables
        dim_vars = [col for col in self.fact_df.columns 
                   if col not in MEASURE_VARS and col not in EXCLUDE_VARS]
        
        # Process each variable that needs a dimension table
        for var_name in dim_vars:
            if var_name not in self.ipums_vars:
                print(f"Warning: {var_name} not found in IPUMS definitions")
                continue
                
            var_info = self.ipums_vars[var_name]
            print(f"Creating dimension table for {var_name}...")
            print(f"  Description: {var_info['desc']}")
            
            # Create dimension table from IPUMS codes
            dim_data = []
            for code, description in var_info['codes'].items():
                try:
                    code_val = int(code)
                except ValueError:
                    code_val = code
                    
                dim_data.append({
                    var_name: code_val,
                    f'{var_name}_value': description,
                    f'{var_name}_desc': var_info['desc']
                })
            
            dim_df = pd.DataFrame(dim_data)
            
            # Add any values found in data but not in IPUMS definitions
            actual_values = set(self.fact_df[var_name].unique())
            defined_values = set(dim_df[var_name].unique())
            missing_values = actual_values - defined_values
            
            if missing_values:
                print(f"  Warning: Found {len(missing_values)} values in data not in IPUMS definitions")
                for val in sorted(missing_values):
                    dim_data.append({
                        var_name: val,
                        f'{var_name}_value': f'Undefined code: {val}',
                        f'{var_name}_desc': var_info['desc']
                    })
                dim_df = pd.DataFrame(dim_data)
            
            # Sort by code value
            dim_df = dim_df.sort_values(var_name)
            
            # Save dimension table
            dim_file = self.output_dir / f'dim_{var_name.lower()}.csv'
            dim_df.to_csv(dim_file, index=False)
            print(f"  - Saved {dim_file} with {len(dim_df)} records")
    
    def save_fact_table(self):
        """Save the fact table in ZIP format."""
        # Remove excluded variables from fact table
        for var in EXCLUDE_VARS:
            if var in self.fact_df.columns:
                self.fact_df = self.fact_df.drop(columns=[var])
        
        fact_file = self.output_dir / 'fact_acs_2023.csv.zip'
        self.fact_df.to_csv(
            fact_file,
            index=False,
            compression={'method': 'zip', 'archive_name': 'fact_acs_2023.csv'}
        )
        print(f"\nSaved fact table: {fact_file} with {len(self.fact_df):,} records")
        print(f"Fact table columns: {', '.join(self.fact_df.columns)}")
    
    def print_schema_structure(self):
        """Print the star schema structure."""
        print("\nStar Schema Structure:")
        print("=====================")
        
        print("Fact Table:")
        print(f"  - fact_acs_2023.csv.zip ({len(self.fact_df):,} records)")
        print("  - Measures:")
        for var in MEASURE_VARS:
            if var in self.fact_df.columns:
                print(f"    * {var}")
        
        print("\nDimension Tables:")
        dim_vars = [col for col in self.fact_df.columns 
                   if col not in MEASURE_VARS and col not in EXCLUDE_VARS]
        
        for var in sorted(dim_vars):
            if var in self.ipums_vars:
                print(f"  * dim_{var.lower()}.csv: {self.ipums_vars[var]['desc']}")
            else:
                print(f"  * dim_{var.lower()}.csv (no IPUMS definition available)")
    
    def create_schema(self):
        """Create the complete star schema."""
        try:
            self.load_data()
            # Create dimensions from IPUMS definitions
            self.create_dimension_tables()
            # Save fact table
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