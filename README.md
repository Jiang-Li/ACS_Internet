# Internet Access and Census Data Analysis Project

## Overview
This project analyzes American Community Survey (ACS) data from IPUMS USA, focusing on internet access, demographic characteristics, and socioeconomic indicators across the United States.

## Data Source
The data is sourced from IPUMS USA, University of Minnesota (www.ipums.org). The dataset combines:
- American Community Survey (ACS) responses
- Census data from 1850-2013
- Detailed variables on internet access, demographics, and socioeconomic status

## Project Structure
```
.
├── data/
│   └── raw/
│       └── ipums_variables.xml  # Original IPUMS variable definitions
├── docs/
│   └── variables.md            # Detailed documentation of all variables
└── README.md                   # This file
```

## Variables
The dataset includes 26 key variables across several categories:

### Geographic Variables
- YEAR: Census year (1850-2013)
- REGION: Census region and division
- STATEFIP: State FIPS codes

### Internet Access Variables
- CINETHH: Access to internet
- CILAPTOP: Laptop/desktop computer access
- CISMRTPHN: Smartphone access
- CITABLET: Tablet access
- CIDATAPLN: Cellular data plan
- CIHISPEED: Broadband internet service
- CISAT: Satellite internet service

### Demographic Variables
- PERNUM: Person number in sample unit
- PERWT: Person weight
- SEX: Sex
- AGE: Age
- RACE: Race (general version)
- RACED: Race (detailed version)
- LANGUAGED: Language spoken (detailed)

### Socioeconomic Variables
- HHINCOME: Total household income
- INCTOT: Total personal income
- EDUCD: Educational attainment
- EMPSTAT: Employment status
- EMPSTATD: Detailed employment status

### Disability Variables
- DIFFREM: Cognitive difficulty
- DIFFCARE: Self-care difficulty
- DIFFSENS: Vision/hearing difficulty
- DIFFEYE: Vision difficulty

## Documentation
For detailed information about each variable, including:
- Technical specifications
- Valid values and codes
- Special notes and considerations
- Historical changes

Please refer to [docs/variables.md](docs/variables.md).

## Data Format
The data is structured as a fixed-width file where each variable occupies specific column positions. The complete layout of all variables is documented in the technical details section of [docs/variables.md](docs/variables.md).

## Usage Notes
1. Income variables (HHINCOME, INCTOT) are in contemporary dollars and must be adjusted for inflation using CPI99 for temporal analysis
2. Person weights (PERWT) should be used for population-representative analyses
3. Multiple race categories are available from 2000 onward
4. Internet access variables are only available in recent survey years

## Citation
When using this data, please cite:
Steven Ruggles, Sarah Flood, Matthew Sobek, Danika Brockman, Grace Cooper, Stephanie Richards, and Megan Schouweiler. IPUMS USA: Version 13.0 [dataset]. Minneapolis, MN: IPUMS, 2023.
https://doi.org/10.18128/D010.V13.0