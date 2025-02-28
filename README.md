# Internet Access Analysis from ACS Data

This project analyzes internet access and smartphone usage patterns across the United States using American Community Survey (ACS) data. It processes the data using a star schema approach and generates weighted statistics by state and education level.

## Project Structure

```
InternetACSData/
├── src/
│   ├── analysis/
│   │   ├── analyze_weighted_stats.py   # Main analysis script
│   │   └── results/                    # Analysis output files
│   └── schema/
│       └── create_star_schema.py       # Star schema creation script
├── star_schema/                        # Processed dimensional tables
│   ├── fact_acs_2023.csv              # Main fact table
│   ├── dim_statefip.csv               # State dimension
│   ├── dim_educ.csv                   # Education dimension
│   └── ...                            # Other dimension tables
├── results/                           # Analysis results
│   ├── internet_smartphone_by_state.csv
│   ├── internet_smartphone_by_education.csv
│   └── analysis_report.txt
└── requirements.txt                   # Project dependencies
```

## Features

- **Star Schema Data Model**:
  - Fact table with person-level records
  - Dimension tables for states, education levels, and demographics
  - Population weights (PERWT) for accurate estimates

- **Analysis Capabilities**:
  - Weighted internet access rates by state
  - Weighted smartphone usage by state
  - Technology access by education level
  - Digital divide analysis
  - Population-weighted statistics

## Requirements

```bash
pip install -r requirements.txt
```

## Usage

1. Create the star schema:
```bash
python src/schema/create_star_schema.py
```

2. Run the analysis:
```bash
python src/analysis/analyze_weighted_stats.py
```

## Analysis Outputs

The analysis generates three main files in the `results` directory:

1. `internet_smartphone_by_state.csv`:
   - State-level statistics
   - Internet access percentages
   - Smartphone usage percentages
   - Population estimates

2. `internet_smartphone_by_education.csv`:
   - Education level statistics
   - Internet access percentages
   - Smartphone usage percentages
   - Population estimates by education level

3. `analysis_report.txt`:
   - Detailed findings
   - National averages
   - Top/bottom states
   - Digital divide metrics
   - Education level correlations

## Methodology

The analysis uses person weights (PERWT) from the ACS to calculate representative statistics:
1. Filters out missing/invalid values
2. Applies population weights for accurate estimates
3. Aggregates by state and education level
4. Calculates weighted percentages for internet and smartphone access

## Data Source

Data comes from the IPUMS USA American Community Survey (ACS) 2023, focusing on:
- Internet access (CINETHH)
- Smartphone usage (CISMRTPHN)
- Educational attainment (EDUC)
- State of residence (STATEFIP)
- Person weights (PERWT)

## License

This project is licensed under the MIT License.

## Acknowledgments

- Data source: IPUMS USA, American Community Survey 2023