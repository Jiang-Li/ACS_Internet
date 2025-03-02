"""
Analyze internet access patterns across demographic dimensions from ACS data.
This script calculates weighted statistics for internet access by various 
demographic, geographic, and socioeconomic factors.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Get the project root directory (1 level up from this script)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def create_income_buckets(income_data):
    """Create income buckets using a combination of quantiles and manual ranges.
    
    Args:
        income_data (pd.Series): Series containing income values
        
    Returns:
        pd.Series: Categorical series with income buckets
    """
    # Handle negative and zero incomes separately
    income_data = income_data.copy()
    income_data = income_data.clip(lower=0)
    
    # Define quantiles for positive incomes
    n_quantiles = 7  # Number of buckets for positive incomes
    
    try:
        # Create buckets for positive incomes
        positive_mask = income_data > 0
        if positive_mask.any():
            buckets = pd.qcut(
                income_data[positive_mask],
                q=n_quantiles,
                labels=[
                    'Very Low Income',
                    'Low Income',
                    'Lower Middle',
                    'Middle',
                    'Upper Middle',
                    'High',
                    'Very High'
                ],
                duplicates='drop'
            )
            
            # Create final series with both zero and positive incomes
            result = pd.Series(index=income_data.index, dtype='category')
            result[income_data == 0] = 'No Income'
            result[positive_mask] = buckets
            
            return result
        else:
            return pd.Series('No Income', index=income_data.index)
            
    except Exception as e:
        logging.error(f"Error creating income buckets: {str(e)}")
        # Fallback to simpler bucketing if the above fails
        return pd.cut(
            income_data,
            bins=[-np.inf, 0, 20000, 40000, 60000, 100000, np.inf],
            labels=['No Income', 'Very Low', 'Low', 'Middle', 'High', 'Very High']
        )

def load_and_prepare_data(data_dir=None):
    """Load and prepare the ACS data for internet access analysis.
    
    Loads the fact table and dimension tables, creates age and income buckets,
    and filters out invalid internet access records.
    
    Args:
        data_dir (str or Path, optional): Directory containing the star schema data.
            Defaults to PROJECT_ROOT/data/processed/star_schema.
            
    Returns:
        tuple: (internet_data, dimension_tables)
            - internet_data (pd.DataFrame): Prepared fact table with:
                - Filtered valid internet records
                - Age buckets
                - Income buckets
            - dimension_tables (dict): Dictionary of dimension DataFrames
    """
    if data_dir is None:
        data_dir = PROJECT_ROOT / 'data/processed/star_schema'
    data_dir = Path(data_dir)
    
    logging.info(f"Loading data from: {data_dir}")
    
    try:
        # Read the fact table
        internet_data = pd.read_csv(
            data_dir / 'fact_acs_2023.csv.zip',
            compression={'method': 'zip', 'archive_name': 'fact_acs_2023.csv'}
        )
        
        # Load all dimension tables into a dictionary
        dimension_tables = {
            dim_file.stem.replace('dim_', ''): pd.read_csv(dim_file)
            for dim_file in data_dir.glob('dim_*.csv')
        }
        
        # Filter for valid internet records (9 indicates missing/invalid)
        internet_data = internet_data[internet_data['CINETHH'] != 9]
        
        # Create age buckets for demographic analysis
        age_bins = [0, 18, 25, 35, 50, 65, 100]
        age_labels = ['0-18', '19-25', '26-35', '36-50', '51-65', '65+']
        internet_data['AGE_BUCKET'] = pd.cut(
            internet_data['AGE'],
            bins=age_bins,
            labels=age_labels
        )
        
        # Create income buckets
        internet_data['INCTOT_BUCKET'] = create_income_buckets(internet_data['INCTOT'])
        
        logging.info(f"Successfully loaded {len(internet_data):,} valid records")
        return internet_data, dimension_tables
        
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
        raise

def calculate_weighted_access_stats(data_frame, group_col, weight_col='PERWT', access_col='CINETHH'):
    """Calculate weighted internet access statistics for a grouping variable.
    
    Uses vectorized operations to compute weighted percentages and population estimates
    for each unique value in the grouping column.
    
    Args:
        data_frame (pd.DataFrame): DataFrame containing the analysis data
        group_col (str): Column name to group by
        weight_col (str, optional): Column containing weights. Defaults to 'PERWT'.
        access_col (str, optional): Column indicating internet access. Defaults to 'CINETHH'.
    
    Returns:
        pd.DataFrame: Statistics for each group with columns:
            - dimension_value: The grouping value
            - internet_percentage: Weighted percentage with internet access
            - population_estimate: Weighted population estimate
    """
    # Group by the dimension and calculate statistics
    grouped_stats = data_frame.groupby(group_col).agg({
        weight_col: 'sum',  # Total weight for population estimate
        access_col: lambda x: np.average(x == 1, weights=data_frame.loc[x.index, weight_col])
    }).reset_index()
    
    # Rename columns for clarity
    grouped_stats.columns = ['dimension_value', 'population_estimate', 'internet_percentage']
    
    # Convert percentage to 0-100 scale
    grouped_stats['internet_percentage'] *= 100
    
    return grouped_stats.sort_values('internet_percentage', ascending=False)

def merge_dimension_descriptions(stats_df, dim_table, dim_name):
    """Merge dimension descriptions with statistics.
    
    Args:
        stats_df (pd.DataFrame): Statistics DataFrame
        dim_table (pd.DataFrame): Dimension table with descriptions
        dim_name (str): Name of the dimension
        
    Returns:
        pd.DataFrame: Statistics with merged descriptions
    """
    if dim_name not in ['AGE_BUCKET', 'INCTOT_BUCKET']:
        dim_col = dim_name.upper()
        value_col = f"{dim_col}_value"
        
        if value_col in dim_table.columns:
            return pd.merge(
                stats_df,
                dim_table[[dim_col, value_col]],
                left_on='dimension_value',
                right_on=dim_col,
                how='left'
            )
    
    return stats_df

def create_bar_plot(data, x_col, y_col, title, rotate_labels=45):
    """Create a bar plot using seaborn.
    
    Args:
        data (pd.DataFrame): Data to plot
        x_col (str): Column for x-axis
        y_col (str): Column for y-axis
        title (str): Plot title
        rotate_labels (int, optional): Degrees to rotate x-axis labels. Defaults to 45.
    """
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    
    plot = sns.barplot(
        data=data,
        x=x_col,
        y=y_col,
        color='skyblue'
    )
    
    plt.title(title)
    plt.xlabel(x_col.replace('_', ' ').title())
    plt.ylabel("Internet Access (%)")
    plt.xticks(rotation=rotate_labels)
    plt.tight_layout()

def save_dimension_plot(data_frame, dim_name, plots_dir):
    """Create and save a visualization for a dimension's analysis.
    
    Args:
        data_frame (pd.DataFrame): Analysis results
        dim_name (str): Name of the dimension
        plots_dir (Path): Directory to save plots
    
    Returns:
        str: Relative path to the saved plot
    """
    # Determine x-axis column and title
    x_col = 'STATEFIP_value' if dim_name == 'statefip' and 'STATEFIP_value' in data_frame.columns else 'dimension_value'
    title = f"Internet Access by {dim_name.replace('_', ' ').title()}"
    
    # Create appropriate plot type
    if dim_name == 'statefip':
        create_bar_plot(data_frame, x_col, 'internet_percentage', title, rotate_labels=90)
    elif dim_name in ['AGE_BUCKET', 'INCTOT_BUCKET']:
        create_bar_plot(data_frame, x_col, 'internet_percentage', title, rotate_labels=45)
    else:
        create_bar_plot(data_frame, x_col, 'internet_percentage', title, rotate_labels=45)
    
    # Save plot
    plot_path = plots_dir / f"{dim_name}_internet_access.png"
    plt.savefig(plot_path)
    plt.close()
    
    return f"plots/{plot_path.name}"

def analyze_dimension(internet_data, dim_table, dim_name):
    """Analyze internet access patterns for a specific dimension.
    
    Args:
        internet_data (pd.DataFrame): Prepared fact table
        dim_table (pd.DataFrame): Dimension table
        dim_name (str): Name of the dimension
        
    Returns:
        pd.DataFrame: Analysis results
    """
    logging.info(f"Analyzing internet access by {dim_name}")
    
    # Use the original column name for grouping
    group_col = dim_name if dim_name in ['AGE_BUCKET', 'INCTOT_BUCKET'] else dim_name.upper()
    
    # Calculate statistics using vectorized operations
    access_stats = calculate_weighted_access_stats(internet_data, group_col)
    
    # Merge with dimension descriptions if available
    return merge_dimension_descriptions(access_stats, dim_table, dim_name)

def generate_markdown_report(analysis_results, report_file):
    """Generate a markdown report with analysis results and plots.
    
    Args:
        analysis_results (dict): Dictionary of analysis results by dimension
        report_file (Path): Path to save the report
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_sections = [
        "# Internet Access Analysis Report",
        f"Generated: {timestamp}",
        "",
        "## Overview",
        "Analysis of internet access patterns across various demographic dimensions.",
        "",
    ]
    
    # Add sections for each dimension
    for dim_name, results in analysis_results.items():
        section_title = dim_name.replace('_', ' ').title()
        report_sections.extend([
            f"## {section_title} Analysis",
            "",
            f"![{section_title} Internet Access]({results['plot_path']})",
            "",
            "### Key Findings",
            f"- Highest access: {results['highest_access']:.1f}%",
            f"- Lowest access: {results['lowest_access']:.1f}%",
            f"- Range: {results['access_range']:.1f} percentage points",
            "",
        ])
    
    # Write report
    report_file.parent.mkdir(exist_ok=True)
    report_file.write_text('\n'.join(report_sections))
    logging.info(f"Report generated: {report_file}")

def main():
    """Main function to run the internet access analysis pipeline."""
    try:
        # Create output directories
        results_dir = PROJECT_ROOT / 'results'
        plots_dir = results_dir / 'plots'
        plots_dir.mkdir(parents=True, exist_ok=True)
        
        # Load and prepare data
        internet_data, dimension_tables = load_and_prepare_data()
        
        # Define dimensions to analyze
        dimensions = [
            'statefip', 'region', 'educ', 'race', 'sex', 'empstat',
            'language', 'diffeye', 'diffsens', 'diffcare', 'diffrem',
            'AGE_BUCKET', 'INCTOT_BUCKET'
        ]
        
        # Analyze each dimension
        analysis_results = {}
        for dim_name in dimensions:
            # Get dimension table if available
            dim_table = dimension_tables.get(dim_name, pd.DataFrame())
            
            # Analyze dimension and create visualization
            results_df = analyze_dimension(internet_data, dim_table, dim_name)
            plot_path = save_dimension_plot(results_df, dim_name, plots_dir)
            
            # Store results
            analysis_results[dim_name] = {
                'results': results_df,
                'plot_path': plot_path,
                'highest_access': results_df['internet_percentage'].max(),
                'lowest_access': results_df['internet_percentage'].min(),
                'access_range': results_df['internet_percentage'].max() - 
                               results_df['internet_percentage'].min()
            }
        
        # Generate report
        report_file = results_dir / 'report.md'
        generate_markdown_report(analysis_results, report_file)
        
    except Exception as e:
        logging.error(f"An error occurred during analysis: {str(e)}")
        raise

if __name__ == '__main__':
    main() 