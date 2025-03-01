# Internet ACS Data Star Schema

This project transforms American Community Survey (ACS) data into a star schema format, focusing on internet access and related variables.

## Star Schema Structure

### Fact Table
The fact table (`fact_acs_2023.csv.zip`) contains the following:

#### Measures
These are the quantitative variables in the fact table:
- `PERWT`: Person weight for the observation
- `AGE`: Person's age in years
- `HHINCOME`: Total household income
- `INCTOT`: Total personal income

### Dimension Tables
All non-measure variables (except YEAR and PERNUM) are transformed into dimension tables. Each dimension table is named `dim_<variable_name>.csv` and contains:
- The variable code (key)
- The value description
- The variable description

Each dimension table follows this structure:
```
<variable_name>, <variable_name>_value, <variable_name>_desc
code,           "description",         "variable description"
```

## Requirements

1. **Fact Table Requirements**:
   - Contains only the original data (except YEAR and PERNUM are removed)
   - Preserves the four measure variables (PERWT, AGE, HHINCOME, INCTOT)
   - All other variables must have corresponding dimension tables

2. **Dimension Tables Requirements**:
   - Must be created for all non-measure variables in the fact table
   - Must use definitions from the IPUMS XML file
   - Must include both the code and its meaning
   - Must include the variable description

## Data Sources

- Input data: `data/raw/usa_2023_subset.csv.zip`
- Variable definitions: `data/raw/ipums_variables.xml`
- Output directory: `data/processed/star_schema/`

## Usage

Run the star schema creation script:
```bash
python src/create_star_schema.py
```

This will:
1. Read the input CSV data
2. Load variable definitions from the XML file
3. Create dimension tables for all categorical variables
4. Create the fact table with measures and dimension keys
5. Save all tables in the output directory

## Data Structure

The data is organized in a star schema with one fact table and multiple dimension tables.

### Fact Table (`fact_person.csv.zip`)

The fact table contains all original columns from the ACS data, including:
- Measures:
  - `PERWT`: Person weight for the observation
  - `AGE`: Person's age in years
  - `HHINCOME`: Total household income
  - `INCTOT`: Total personal income
- Foreign keys to dimension tables (all other columns)

### Dimension Tables

Each dimension table is stored as a CSV file with `_id` and `_label` columns.

#### Geographic Dimensions
- `dim_region.csv`: Census regions and divisions
- `dim_statefip.csv`: States (FIPS codes)

#### Internet Access Dimensions
- `dim_cinethh.csv`: Internet access in household
- `dim_cilaptop.csv`: Laptop/desktop computer access
- `dim_cismrtphn.csv`: Smartphone access
- `dim_citablet.csv`: Tablet access
- `dim_cidatapln.csv`: Data plan access
- `dim_cihispeed.csv`: High-speed internet access
- `dim_cisat.csv`: Satellite internet access

#### Demographic Dimensions
- `dim_sex.csv`: Sex/gender
- `dim_race.csv`: Basic race categories
- `dim_raced.csv`: Detailed race categories
- `dim_language.csv`: Basic language categories
- `dim_languaged.csv`: Detailed language categories

#### Education and Employment Dimensions
- `dim_educ.csv`: Basic educational attainment
- `dim_educd.csv`: Detailed educational attainment
- `dim_empstat.csv`: Basic employment status
- `dim_empstatd.csv`: Detailed employment status

#### Disability Dimensions
- `dim_diffrem.csv`: Cognitive difficulty
- `dim_diffcare.csv`: Self-care difficulty
- `dim_diffsens.csv`: Vision or hearing difficulty
- `dim_diffeye.csv`: Vision difficulty

### Excluded Variables
The following variables are not used as dimension tables:
- `YEAR`: Reference year (2023)
- `PERNUM`: Person number within household
- `PERWT`: Person weight (used as measure)
- `AGE`: Age in years (used as measure)

## Variable Formatting

Special formatting is applied to certain variables:
- Four-digit codes: `LANGUAGED`, `RACED`
- Three-digit codes: `STATEFIP`, `EDUCD`
- Two-digit codes: `EDUC`, `EMPSTATD`, `CIHISPEED`
- Continuous values: `HHINCOME`, `INCTOT` (formatted with commas)

## Usage

The star schema can be used to analyze:
1. Internet access patterns across different demographic groups
2. Educational and employment characteristics of households with different types of internet access
3. Geographic variations in internet access and device availability
4. Relationships between income levels and internet/device access
5. Disability status and internet accessibility

## Data Processing

The star schema is created using the script `src/schema/create_star_schema.py`. The script:
1. Reads the raw ACS data from `data/raw/usa_2023_subset.csv.zip`
2. Extracts variable definitions from `data/raw/ipums_variables.xml`
3. Creates dimension tables with proper labels from the XML definitions
4. Saves all tables to the `data/processed/` directory

## Project Structure

```
InternetACSData/
├── data/
│   ├── raw/
│   │   ├── usa_2023_subset.csv.zip    # Input ACS data
│   │   └── ipums_variables.xml        # Variable definitions
│   └── processed/                     # Output directory
│       ├── fact_person.csv.zip        # Fact table
│       ├── dim_region.csv             # Region dimension
│       ├── dim_statefip.csv           # State dimension
│       ├── dim_educ.csv               # Education dimension
│       └── ...                        # Other dimension tables
└── src/
    └── schema/
        ├── create_star_schema.py      # Star schema creation script
        └── analyze_variables.py       # Variable analysis script
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

- Python 3.x
- pandas
- numpy

## Running the Code

Create the star schema:
```bash
python3 src/schema/create_star_schema.py
```

The script will:
1. Read the input data from `data/raw/`
2. Create dimension tables with labels from XML definitions
3. Save all tables to `data/processed/`

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