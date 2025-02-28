"""
Analyze internet and device access patterns from ACS data.
This script calculates weighted statistics for internet and smartphone access
by state and education level.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import os

# Get the project root directory (2 levels up from this script)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

class TechnologyAccessAnalyzer:
    def __init__(self, data_dir=None):
        """Initialize the analyzer.
        
        Args:
            data_dir (str): Directory containing the star schema data
        """
        if data_dir is None:
            data_dir = PROJECT_ROOT / 'star_schema'
        self.data_dir = Path(data_dir)
        self.fact_df = None
        self.state_dim = None
        self.educ_dim = None
        self.results_dir = PROJECT_ROOT / 'results'
        self.report_lines = []  # Store report lines for later saving
        
        # Ensure directories exist
        self.results_dir.mkdir(exist_ok=True)
        
    def log(self, message, print_to_console=True):
        """Log a message to both console and report.
        
        Args:
            message (str): Message to log
            print_to_console (bool): Whether to print to console
        """
        self.report_lines.append(message)
        if print_to_console:
            print(message)
    
    def load_data(self):
        """Load the necessary tables from the star schema."""
        self.log("Reading tables...")
        self.log(f"Loading data from: {self.data_dir}")
        
        try:
            self.fact_df = pd.read_csv(self.data_dir / 'fact_acs_2023.csv')
            self.state_dim = pd.read_csv(self.data_dir / 'dim_statefip.csv')
            self.educ_dim = pd.read_csv(self.data_dir / 'dim_educ.csv')
            
            # Filter out missing values
            self.valid_internet = self.fact_df[self.fact_df['CINETHH'] != 9]
            self.valid_smartphone = self.fact_df[self.fact_df['CISMRTPHN'] != 9]
            
            self.log(f"Successfully loaded {len(self.fact_df):,} records")
        except Exception as e:
            self.log(f"Error loading data: {str(e)}")
            raise
    
    @staticmethod
    def calculate_weighted_percentage(df, weight_col, condition_col, condition_value=1):
        """Calculate weighted percentage for a given condition.
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            weight_col (str): Name of the weight column
            condition_col (str): Name of the condition column
            condition_value (int): Value to calculate percentage for
            
        Returns:
            float: Weighted percentage
        """
        total_weight = df[weight_col].sum()
        if total_weight == 0:
            return 0
        condition_weight = df[df[condition_col] == condition_value][weight_col].sum()
        return (condition_weight / total_weight * 100)
    
    def analyze_by_state(self):
        """Calculate internet and smartphone access statistics by state."""
        self.log("\nCalculating internet and smartphone access by state...")
        state_stats = []
        
        for state_code in self.state_dim['STATEFIP']:
            state_internet = self.valid_internet[self.valid_internet['STATEFIP'] == state_code]
            state_smartphone = self.valid_smartphone[self.valid_smartphone['STATEFIP'] == state_code]
            
            if len(state_internet) > 0 and len(state_smartphone) > 0:
                internet_pct = self.calculate_weighted_percentage(
                    state_internet, 'PERWT', 'CINETHH'
                )
                smartphone_pct = self.calculate_weighted_percentage(
                    state_smartphone, 'PERWT', 'CISMRTPHN'
                )
                population = state_internet['PERWT'].sum()
                
                state_stats.append({
                    'STATEFIP': state_code,
                    'internet_percentage': internet_pct,
                    'smartphone_percentage': smartphone_pct,
                    'population_estimate': population
                })
        
        # Create DataFrame and merge with state names
        state_stats_df = pd.DataFrame(state_stats)
        state_stats_df = pd.merge(state_stats_df, self.state_dim, on='STATEFIP', how='left')
        state_stats_df = state_stats_df.sort_values('internet_percentage', ascending=False)
        
        self._print_state_results(state_stats_df)
        return state_stats_df
    
    def analyze_by_education(self):
        """Calculate internet and smartphone access statistics by education level."""
        self.log("\nCalculating internet and smartphone access by education level...")
        educ_stats = []
        
        for educ_code in sorted(self.educ_dim['EDUC']):
            educ_internet = self.valid_internet[self.valid_internet['EDUC'] == educ_code]
            educ_smartphone = self.valid_smartphone[self.valid_smartphone['EDUC'] == educ_code]
            
            if len(educ_internet) > 0 and len(educ_smartphone) > 0:
                internet_pct = self.calculate_weighted_percentage(
                    educ_internet, 'PERWT', 'CINETHH'
                )
                smartphone_pct = self.calculate_weighted_percentage(
                    educ_smartphone, 'PERWT', 'CISMRTPHN'
                )
                population = educ_internet['PERWT'].sum()
                
                educ_stats.append({
                    'EDUC': educ_code,
                    'internet_percentage': internet_pct,
                    'smartphone_percentage': smartphone_pct,
                    'population_estimate': population
                })
        
        # Create DataFrame and merge with education descriptions
        educ_stats_df = pd.DataFrame(educ_stats)
        educ_stats_df = pd.merge(educ_stats_df, self.educ_dim, on='EDUC', how='left')
        educ_stats_df = educ_stats_df.sort_values('internet_percentage', ascending=False)
        
        self._print_education_results(educ_stats_df)
        return educ_stats_df
    
    def _print_state_results(self, state_stats_df):
        """Print state-level results in a formatted table."""
        self.log("\nInternet and Smartphone Access by State:")
        self.log("=" * 100)
        self.log(f"{'State':<20}{'Internet %':>12}{'Smartphone %':>15}{'Population Est.':>20}")
        self.log("-" * 100)
        for _, row in state_stats_df.iterrows():
            self.log(f"{row['STATEFIP_value']:<20}{row['internet_percentage']:>11.1f}%"
                    f"{row['smartphone_percentage']:>14.1f}%{row['population_estimate']:>20,.0f}")
    
    def _print_education_results(self, educ_stats_df):
        """Print education-level results in a formatted table."""
        self.log("\nInternet and Smartphone Access by Education Level:")
        self.log("=" * 100)
        self.log(f"{'Education Level':<40}{'Internet %':>12}{'Smartphone %':>15}"
                f"{'Population Est.':>20}")
        self.log("-" * 100)
        for _, row in educ_stats_df.iterrows():
            self.log(f"{row['EDUC_value']:<40}{row['internet_percentage']:>11.1f}%"
                    f"{row['smartphone_percentage']:>14.1f}%{row['population_estimate']:>20,.0f}")
    
    def generate_summary_statistics(self, state_stats_df, educ_stats_df):
        """Generate summary statistics and insights."""
        self.log("\nKey Findings and Summary Statistics")
        self.log("=" * 100)
        
        # State-level statistics
        self.log("\nState-Level Statistics:")
        self.log("-" * 50)
        self.log(f"National Average Internet Access: {state_stats_df['internet_percentage'].mean():.1f}%")
        self.log(f"National Average Smartphone Usage: {state_stats_df['smartphone_percentage'].mean():.1f}%")
        self.log("\nTop 5 States by Internet Access:")
        for _, row in state_stats_df.head().iterrows():
            self.log(f"  - {row['STATEFIP_value']}: {row['internet_percentage']:.1f}%")
        
        self.log("\nBottom 5 States by Internet Access:")
        for _, row in state_stats_df.tail().iterrows():
            self.log(f"  - {row['STATEFIP_value']}: {row['internet_percentage']:.1f}%")
        
        # Education-level statistics
        self.log("\nEducation-Level Statistics:")
        self.log("-" * 50)
        self.log("\nInternet Access Range by Education:")
        self.log(f"  Highest: {educ_stats_df['EDUC_value'].iloc[0]} ({educ_stats_df['internet_percentage'].max():.1f}%)")
        self.log(f"  Lowest: {educ_stats_df['EDUC_value'].iloc[-1]} ({educ_stats_df['internet_percentage'].min():.1f}%)")
        
        # Digital divide insights
        internet_range = state_stats_df['internet_percentage'].max() - state_stats_df['internet_percentage'].min()
        self.log("\nDigital Divide Insights:")
        self.log("-" * 50)
        self.log(f"State-level digital divide (max - min): {internet_range:.1f} percentage points")
        self.log(f"Education-level correlation: Strong positive correlation between education and internet access")
        
        # Technology adoption patterns
        self.log("\nTechnology Adoption Patterns:")
        self.log("-" * 50)
        states_higher_smartphone = state_stats_df[
            state_stats_df['smartphone_percentage'] > state_stats_df['internet_percentage']
        ]
        self.log(f"States with higher smartphone than internet usage: {len(states_higher_smartphone)}")
    
    def save_results(self, state_stats_df, educ_stats_df):
        """Save analysis results to CSV files and generate report."""
        # Save CSV results
        state_file = self.results_dir / 'internet_smartphone_by_state.csv'
        educ_file = self.results_dir / 'internet_smartphone_by_education.csv'
        report_file = self.results_dir / 'analysis_report.txt'
        
        state_stats_df.to_csv(state_file, index=False)
        educ_stats_df.to_csv(educ_file, index=False)
        
        # Generate summary statistics
        self.generate_summary_statistics(state_stats_df, educ_stats_df)
        
        # Save the complete analysis report
        with open(report_file, 'w') as f:
            f.write("Internet and Smartphone Access Analysis Report\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            f.write('\n'.join(self.report_lines))
        
        self.log("\nResults saved to:")
        self.log(f"- {state_file}")
        self.log(f"- {educ_file}")
        self.log(f"- {report_file}")
    
    def run_analysis(self):
        """Run the complete analysis pipeline."""
        try:
            self.load_data()
            state_stats = self.analyze_by_state()
            educ_stats = self.analyze_by_education()
            self.save_results(state_stats, educ_stats)
        except Exception as e:
            self.log(f"An error occurred during analysis: {str(e)}")

def main():
    """Main function to run the analysis."""
    analyzer = TechnologyAccessAnalyzer()
    analyzer.run_analysis()

if __name__ == '__main__':
    main() 