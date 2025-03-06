# IPUMS ACS Variables Documentation

## Overview
This document contains definitions and specifications for all variables in the IPUMS ACS dataset. The data is sourced from IPUMS USA, University of Minnesota (www.ipums.org).

## Variables

### Technical Details
| Variable Name | Description | Type | Start Pos | End Pos | Width | Decimals |
|--------------|-------------|------|-----------|---------|--------|----------|
| YEAR | Census year | Integer (discrete) | 1 | 4 | 4 | 0 |
| REGION | Census region and division | Integer (discrete) | 5 | 6 | 2 | 0 |
| STATEFIP | State (FIPS code) | Integer (discrete) | 7 | 8 | 2 | 0 |
| HHINCOME | Total household income | Integer (continuous) | 9 | 15 | 7 | 0 |
| CINETHH | Access to internet | Integer (discrete) | 16 | 16 | 1 | 0 |
| CILAPTOP | Laptop, desktop, or notebook computer | Integer (discrete) | 17 | 17 | 1 | 0 |
| CISMRTPHN | Smartphone | Integer (discrete) | 18 | 18 | 1 | 0 |
| CITABLET | Tablet or other portable wireless computer | Integer (discrete) | 19 | 19 | 1 | 0 |
| CIDATAPLN | Cellular data plan | Integer (discrete) | 20 | 20 | 1 | 0 |
| CIHISPEED | Broadband internet service | Integer (discrete) | 21 | 22 | 2 | 0 |
| CISAT | Satellite internet service | Integer (discrete) | 23 | 23 | 1 | 0 |
| PERNUM | Person number in sample unit | Integer (continuous) | 24 | 27 | 4 | 0 |
| PERWT | Person weight | Decimal | 28 | 37 | 10 | 2 |
| SEX | Sex | Integer (discrete) | 38 | 38 | 1 | 0 |
| AGE | Age | Integer (discrete) | 39 | 41 | 3 | 0 |
| RACE | Race [general version] | Integer (discrete) | 42 | 42 | 1 | 0 |
| RACED | Race [detailed version] | Integer (discrete) | 43 | 45 | 3 | 0 |
| LANGUAGED | Language spoken [detailed version] | Integer (discrete) | 48 | 51 | 4 | 0 |
| EDUCD | Educational attainment [detailed version] | Integer (discrete) | 54 | 56 | 3 | 0 |
| EMPSTAT | Employment status [general version] | Integer (discrete) | 57 | 57 | 1 | 0 |
| EMPSTATD | Employment status [detailed version] | Integer (discrete) | 58 | 59 | 2 | 0 |
| INCTOT | Total personal income | Integer (continuous) | 60 | 66 | 7 | 0 |
| DIFFREM | Cognitive difficulty | Integer (discrete) | 67 | 67 | 1 | 0 |
| DIFFCARE | Self-care difficulty | Integer (discrete) | 68 | 68 | 1 | 0 |
| DIFFSENS | Vision or hearing difficulty | Integer (discrete) | 69 | 69 | 1 | 0 |
| DIFFEYE | Vision difficulty | Integer (discrete) | 70 | 70 | 1 | 0 |

### Variable Descriptions

#### YEAR
**Description**: Census year - reports the four-digit year when the household was enumerated or included in the census, the ACS, and the PRCS.

**Additional Information**: For the multi-year ACS/PRCS samples, YEAR indicates the last year of data included (e.g., 2007 for the 2005-2007 3-year ACS/PRCS; 2008 for the 2006-2008 3-year ACS/PRCS; and so on). For the actual year of survey in these multi-year data, see MULTYEAR.

**Valid Values**:
| Code | Label |
|------|-------|
| 1850 | 1850 |
| 1860 | 1860 |
| 1870 | 1870 |
| 1880 | 1880 |
| 1900 | 1900 |
| 1910 | 1910 |
| 1920 | 1920 |
| 1930 | 1930 |
| 1940 | 1940 |
| 1950 | 1950 |
| 1960 | 1960 |
| 1970 | 1970 |
| 1980 | 1980 |
| 1990 | 1990 |
| 2000 | 2000 |
| 2001 | 2001 |
| 2002 | 2002 |
| 2003 | 2003 |
| 2004 | 2004 |
| 2005 | 2005 |
| 2006 | 2006 |
| 2007 | 2007 |
| 2008 | 2008 |
| 2009 | 2009 |
| 2010 | 2010 |
| 2011 | 2011 |
| 2012 | 2012 |
| 2013 | 2013 |

#### REGION
**Description**: Census region and division - identifies the region and division where the housing unit was located.

**Additional Information**: States are classified into the 1990 regional and divisional classification system.

**Valid Values**:
| Code | Label |
|------|-------|
| 11 | New England Division |
| 12 | Middle Atlantic Division |
| 13 | Mixed Northeast Divisions (1970 Metro) |
| 21 | East North Central Div. |
| 22 | West North Central Div. |
| 23 | Mixed Midwest Divisions (1970 Metro) |
| 31 | South Atlantic Division |
| 32 | East South Central Div. |
| 33 | West South Central Div. |
| 34 | Mixed Southern Divisions (1970 Metro) |
| 41 | Mountain Division |
| 42 | Pacific Division |
| 43 | Mixed Western Divisions (1970 Metro) |
| 91 | Military/Military reservations |
| 92 | PUMA boundaries cross state lines-1% sample |
| 97 | State not identified |
| 99 | Not identified |

#### STATEFIP
**Description**: State (FIPS code) - reports the state in which the household was located, using the Federal Information Processing Standards (FIPS) coding scheme.

**Additional Information**: The FIPS coding scheme orders the states alphabetically. In the 1980 Urban/Rural sample, STATEFIP identifies state groups that are not available in STATEICP.

**Valid Values**:
| Code | Label |
|------|-------|
| 01 | Alabama |
| 02 | Alaska |
| 04 | Arizona |
| 05 | Arkansas |
| 06 | California |
| 08 | Colorado |
| 09 | Connecticut |
| 10 | Delaware |
| 11 | District of Columbia |
| 12 | Florida |
| 13 | Georgia |
| 15 | Hawaii |
| 16 | Idaho |
| 17 | Illinois |
| 18 | Indiana |
| 19 | Iowa |
| 20 | Kansas |
| 21 | Kentucky |
| 22 | Louisiana |
| 23 | Maine |
| 24 | Maryland |
| 25 | Massachusetts |
| 26 | Michigan |
| 27 | Minnesota |
| 28 | Mississippi |

#### HHINCOME
**Description**: Total household income - reports the total money income of all household members age 15+ during the previous year.

**Additional Information**: The amount equals the sum of all household members' individual incomes (INCTOT). Includes income of all household members present at the time of the census/survey. Amounts are in contemporary dollars and must be adjusted for inflation when studying changes over time. For ACS/PRCS, the reference period is the previous 12 months.

**Special Codes**:
- 9999999: N/A

**Note**: ACS respondents are surveyed throughout the year, and amounts do not reflect calendar year dollars. The Census Bureau provides an adjustment factor (ADJUST) for this purpose.

#### CINETHH
**Description**: Access to internet - reports whether any member of the household accesses the Internet.

**Additional Information**: "Access" refers to whether someone in the household uses or connects to the Internet, regardless of whether they pay for the service.

**Valid Values**:
| Code | Label |
|------|-------|
| 0 | N/A (GQ) |
| 1 | Yes, with a subscription to an Internet Service |
| 2 | Yes, without a subscription to an Internet Service |
| 3 | No Internet access at this house, apartment, or mobile home |

#### CILAPTOP
**Description**: Laptop, desktop, or notebook computer - reports whether the respondent or any member of their household owned or used a desktop, laptop, netbook, or notebook computer.

**Additional Information**: Excludes GPS devices with only limited computed capabilities and household appliances.

**Valid Values**:
| Code | Label |
|------|-------|
| 0 | N/A (GQ) |
| 1 | Yes |
| 2 | No |

#### CISMRTPHN
**Description**: Smartphone - reports whether the respondent or any member of their household owned or used a smartphone.

**Valid Values**:
| Code | Label |
|------|-------|
| 0 | N/A (GQ) |
| 1 | Yes |
| 2 | No |

#### CITABLET
**Description**: Tablet or other portable wireless computer - reports whether the respondent or any member of their household owned or used a tablet or other portable wireless computer.

**Valid Values**:
| Code | Label |
|------|-------|
| 0 | N/A (GQ) |
| 1 | Yes |
| 2 | No |

#### CIDATAPLN
**Description**: Cellular data plan - reports whether the respondent or any member of their household subscribed to the Internet using a cellular data plan for a smartphone or other mobile device.

**Valid Values**:
| Code | Label |
|------|-------|
| 0 | N/A (GQ) |
| 1 | Yes |
| 2 | No |
| 8 | Suppressed for data year 2023 for select PUMAs |

#### CIHISPEED
**Description**: Broadband internet service - reports whether the respondent or any member of their household subscribed to the Internet using broadband (high speed) Internet service.

**Valid Values**:
| Code | Label |
|------|-------|
| 00 | N/A (GQ) |
| 10 | Yes (Cable modem, fiber optic or DSL service) |
| 11 | Cable modem only |
| 12 | Fiber optic only |
| 13 | DSL service only |
| 14 | Cable modem + Fiber optic |
| 15 | Cable modem + DSL service |
| 16 | Fiber optic + DSL service |
| 17 | Cable modem, Fiber optic and DSL service |
| 20 | No |
| 88 | Suppressed for data year 2023 for select PUMAs |

#### CISAT
**Description**: Satellite internet service - reports whether the respondent or any member of their household subscribed to the Internet using a satellite internet service plan.

**Valid Values**:
| Code | Label |
|------|-------|
| 0 | N/A (GQ) |
| 1 | Yes |
| 2 | No |
| 8 | Suppressed for data year 2023 for select PUMAs |

#### PERNUM
**Description**: Person number in sample unit - numbers all persons within each household consecutively in the order in which they appear on the original census or survey form.

**Additional Information**: When combined with SAMPLE and SERIAL, PERNUM uniquely identifies each person within the IPUMS.

#### PERWT
**Description**: Person weight - indicates how many persons in the U.S. population are represented by a given person in an IPUMS sample.

**Additional Information**: Should be used for person-level analysis of most IPUMS samples, except for "flat" or unweighted samples. Values have two implied decimal places (e.g., 010461 = 104.61).

#### SEX
**Description**: Sex - reports whether the person was male or female.

**Valid Values**:
| Code | Label |
|------|-------|
| 1 | Male |
| 2 | Female |
| 9 | Missing/blank |

#### AGE
**Description**: Age - reports the person's age in years as of the last birthday.

**Valid Values**:
| Code | Label |
|------|-------|
| 000 | Less than 1 year old |
| 001-999 | Age in years |

**Note**: There is a known Universe issue with AGE and AGEORIG which affects EMPSTAT and LABFORCE for the 2004 ACS Sample.

#### RACE
**Description**: Race [general version] - provides a general categorization of race responses.

**Additional Information**: Beginning in 2000, respondents could report multiple races. Starting in 2020, the Census Bureau updated the questionnaire text, processing, and coding of race questions, resulting in major changes to the distribution of race categories.

**Valid Values**:
| Code | Label |
|------|-------|
| 1 | White |
| 2 | Black/African American |
| 3 | American Indian or Alaska Native |
| 4 | Chinese |
| 5 | Japanese |
| 6 | Other Asian or Pacific Islander |
| 7 | Other race, nec |
| 8 | Two major races |
| 9 | Three or more major races |

#### RACED
**Description**: Race [detailed version] - provides detailed categorization of race responses.

**Additional Information**: This variable provides more detailed race categories than the general version (RACE). Beginning in 2020, significant changes were made to race question processing and coding.

**Selected Valid Values** (partial list due to extensive categories):
| Code | Label |
|------|-------|
| 100 | White |
| 200 | Black/African American |
| 300 | American Indian/Alaska Native |
| 400 | Chinese |
| 500 | Japanese |
| 600 | Filipino |
| 610 | Asian Indian |
| 620 | Korean |
| 630 | Hawaiian |
| 640 | Vietnamese |
| 650 | Other Asian or Pacific Islander |
| 801 | White and Black |
| 802 | White and AIAN |
| 810 | White and Asian |

Note: RACED includes many more detailed categories for specific tribal affiliations, Asian nationalities, Pacific Islander groups, and various multiracial combinations. The full list contains over 100 categories.

#### LANGUAGED

**Technical Details:**
- Type: Discrete
- Width: 4
- Start Position: 48
- End Position: 51

**Description:**
Reports the language that the respondent spoke at home, particularly if a language other than English was spoken (for the 1910 Puerto Rican sample and the samples from 1980 onward).

**Valid Values:**
| Code | Label |
|------|-------|
| 0000 | N/A or blank |
| 0100 | English |
| 0110 | Jamaican Creole |
| 0120 | Krio, Pidgin Krio |
| 0130 | Hawaiian Pidgin |
| 0140 | Pidgin |
| 0150 | Gullah, Geechee |
| 0160 | Saramacca |
| 0170 | Other English-based Creole languages |
| 0200 | German |
| 0210 | Austrian |
| 0220 | Swiss |
| 0230 | Luxembourgian |
| 0240 | Pennsylvania Dutch |
| 0300 | Yiddish, Jewish |
| 0400 | Dutch |
| 0500 | Swedish |
| 0600 | Danish |
| 0700 | Norwegian |
| 0800 | Icelandic |
| 0900 | Scandinavian |
| 1000 | Italian |
| 1100 | French |
| 1200 | Spanish |
| 1300 | Portuguese |
| 1400 | Rumanian |
| 1500 | Celtic |
| 1600 | Greek |

Note: This is a subset of the most common language codes. The variable includes many more detailed language categories and subcategories.

#### EDUCD

**Technical Details:**
- Type: Discrete
- Width: 3
- Start Position: 54
- End Position: 56

**Description:**
Indicates respondents' educational attainment, as measured by the highest year of school or degree completed. Note that completion differs from the highest year of school attendance; for example, respondents who attended 10th grade but did not finish were classified as having completed 9th grade.

**Valid Values:**
| Code | Label |
|------|-------|
| 000 | N/A or no schooling |
| 002 | No schooling completed |
| 010 | Nursery school to grade 4 |
| 011 | Nursery school, preschool |
| 012 | Kindergarten |
| 013 | Grade 1, 2, 3, or 4 |
| 020 | Grade 5, 6, 7, or 8 |
| 030 | Grade 9 |
| 040 | Grade 10 |
| 050 | Grade 11 |
| 060 | Grade 12 |
| 061 | 12th grade, no diploma |
| 062 | High school graduate or GED |
| 065 | Some college, but less than 1 year |
| 071 | 1 or more years of college credit, no degree |
| 081 | Associate's degree, type not specified |
| 082 | Associate's degree, occupational program |
| 083 | Associate's degree, academic program |
| 101 | Bachelor's degree |
| 114 | Master's degree |
| 115 | Professional degree beyond a bachelor's degree |
| 116 | Doctoral degree |
| 999 | Missing |

#### EMPSTAT

**Technical Details:**
- Type: Discrete
- Width: 1
- Start Position: 57
- End Position: 57

**Description:**
Indicates whether the respondent was a part of the labor force -- working or seeking work -- and, if so, whether the person was currently unemployed. See LABFORCE for a dichotomous variable that identifies whether a person participated in the labor force or not.

**Valid Values:**
| Code | Label |
|------|-------|
| 0 | N/A |
| 1 | Employed |
| 2 | Unemployed |
| 3 | Not in labor force |
| 9 | Unknown/Illegible |

#### EMPSTATD

**Technical Details:**
- Type: Discrete
- Width: 2
- Start Position: 58
- End Position: 59

**Description:**
A detailed version of EMPSTAT that preserves additional related information available for some years. Indicates whether the respondent was a part of the labor force and their specific employment status.

**Valid Values:**
| Code | Label |
|------|-------|
| 00 | N/A |
| 10 | At work |
| 11 | At work, public emerg |
| 12 | Has job, not working |
| 13 | Armed forces |
| 14 | Armed forces--at work |
| 15 | Armed forces--not at work but with job |
| 20 | Unemployed |
| 21 | Unemp, exper worker |
| 22 | Unemp, new worker |
| 30 | Not in Labor Force |
| 31 | NILF, housework |
| 32 | NILF, unable to work |
| 33 | NILF, school |
| 34 | NILF, other |
| 99 | Unknown/Illegible |

#### INCTOT

**Technical Details:**
- Type: Continuous
- Width: 7
- Start Position: 60
- End Position: 66

**Description:**
Reports each respondent's total pre-tax personal income or losses from all sources for the previous year. For Census data, this refers to the previous calendar year; for ACS/PRCS, it refers to the past 12 months. Amounts are in contemporary dollars and must be adjusted for inflation using the CPI99 variable.

**Note:** ACS respondents are surveyed throughout the year, and amounts do not reflect calendar year dollars. The Census Bureau provides an adjustment factor (ADJUST) for this purpose.

**Special Codes:**
- -19998: Bottom code (ACS/PRCS)
- 0: None
- 1: $1 or break even (2000, 2005-onward ACS and PRCS)
- 9999999: N/A
- 9999998: Unknown

#### DIFFREM

**Technical Details:**
- Type: Discrete
- Width: 1
- Start Position: 67
- End Position: 67

**Description:**
Indicates whether the respondent has cognitive difficulties (such as learning, remembering, concentrating, or making decisions) because of a physical, mental, or emotional condition.

**Valid Values:**
| Code | Label |
|------|-------|
| 0 | N/A |
| 1 | No cognitive difficulty |
| 2 | Has cognitive difficulty |

#### DIFFCARE

**Technical Details:**
- Type: Discrete
- Width: 1
- Start Position: 68
- End Position: 68

**Description:**
Indicates whether respondents have any physical or mental health condition that has lasted at least 6 months and makes it difficult for them to take care of their own personal needs, such as bathing, dressing, or getting around inside the home.

**Valid Values:**
| Code | Label |
|------|-------|
| 0 | N/A |
| 1 | No |
| 2 | Yes |

#### DIFFSENS

**Technical Details:**
- Type: Discrete
- Width: 1
- Start Position: 69
- End Position: 69

**Description:**
Indicates whether the respondent has a long-lasting condition of blindness, deafness, or a severe vision or hearing impairment.

**Valid Values:**
| Code | Label |
|------|-------|
| 0 | N/A |
| 1 | No vision or hearing difficulty |
| 2 | Has vision or hearing difficulty |

#### DIFFEYE

**Technical Details:**
- Type: Discrete
- Width: 1
- Start Position: 70
- End Position: 70

**Description:**
Indicates whether the respondent is blind or has serious difficulty seeing even with corrective lenses.

**Valid Values:**
| Code | Label |
|------|-------|
| 0 | N/A |
| 1 | No |
| 2 | Yes |

--- 